"""
This deals with deployment for the Royal Free.

Before you being make sure that in ../private_settings.json
you have
    1) a db_password
    2) an empty dictionary called additional_settings or a dictionary
       of any other variables you want set in your local settings

Make sure the you have a back up directory which is read writeable
that is at BACKUP_DIR

Make sure you have a deployment env that has fabric available

e.g.
workon elcid-deployment or another environment
fab clone_branch your-branch
cd /usr/lib/ohc/elcidrfh-{your branch name}

Then 2 choices

deploy_test, this takes the back up file and name of the new branch.
the back up file will be loaded the environment a database back up from

deploy_prod, this takes the old env and the new env

2 small tasks to look at
create_private_settings will create an empty private settings file in
the appropriate place with the fields for you to fill in

The log environment for this project is considered to be
/usr/lib/ohc/log/

The backups are stored in
/usr/lib/ohc/var/

"""
from __future__ import print_function
import datetime
import json
import copy
import random
from jinja2 import Environment, FileSystemLoader

from fabric.api import local, env

from fabric.context_managers import lcd, settings
from fabric.decorators import task
import os
import stat


"""
3+ hour deployments with 95% time spent backing up and loading a database
are unsustainable.

A rewrite of this process moves to altering in place, with only rollbacks requiring a database load.
"""

env.hosts = ['127.0.0.1']
UNIX_USER = "ohc"
DB_USER = "ohc"
RELEASE_NAME = "elcidrfh-{branch}"

VIRTUAL_ENV_PATH = "/home/{unix_user}/.virtualenvs/{env_name}"
PROJECT_ROOT = "/usr/lib/{unix_user}".format(unix_user=UNIX_USER)
PROJECT_DIRECTORY = "{project_root}/{release_name}"
BACKUP_DIR = "{project_root}/var".format(project_root=PROJECT_ROOT)
GIT_URL = "https://github.com/openhealthcare/elcid-rfh"
LOG_DIR = "/usr/lib/{}/log/".format(UNIX_USER)
# the daily back up
BACKUP_FILE_NAME = "back.{dt}.{db_name}.sql.gz"
BACKUP_NAME = "{backup_dir}/{backup_file_name}"

# the release back up is take just before the release, and then restored
RELEASE_BACKUP_NAME = "{backup_dir}/release.{dt}.{db_name}.sql.gz"

MODULE_NAME = "elcid"
PROJECT_NAME = MODULE_NAME
CRON_TEST_LOAD = "/etc/cron.d/{0}_batch_test_load".format(PROJECT_NAME)
BACKUP_DT_FORMAT = "%d.%m.%Y"

DB_COMMAND_PREFIX = "sudo -u postgres psql --command"
TEMPLATE_DIR = os.path.abspath(os.path.dirname(__file__))
PRIVATE_SETTINGS = "{project_root}/private_settings.json".format(
    project_root=PROJECT_ROOT
)
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class FabException(Exception):
    pass


class Env(object):
    def __init__(self, branch):
        self.branch = branch
        self.release_backup_name = self.get_release_backup_name()

    @property
    def project_directory(self):
        return PROJECT_DIRECTORY.format(
            project_root=PROJECT_ROOT,
            release_name=self.release_name,
        )

    @property
    def release_name(self):
        return RELEASE_NAME.format(branch=self.branch)

    @property
    def virtual_env_path(self):
        return VIRTUAL_ENV_PATH.format(
            unix_user=UNIX_USER,
            env_name=self.release_name
        )

    @property
    def deployment_env_name(self):
        return "{}-deployment".format(self.release_name)

    @property
    def deployment_env_path(self):
        return VIRTUAL_ENV_PATH.format(
            unix_user=UNIX_USER,
            env_name=self.deployment_env_name
        )

    @property
    def database_name(self):
        return self.release_name.replace("-", "_").replace(".", "")

    @property
    def backup_file_name(self):
        now = datetime.datetime.now()
        return BACKUP_FILE_NAME.format(
            dt=now.strftime(BACKUP_DT_FORMAT),
            db_name=self.database_name
        )

    @property
    def backup_name(self):
        return BACKUP_NAME.format(
            backup_dir=BACKUP_DIR,
            backup_file_name=self.backup_file_name
        )

    def get_release_backup_name(self):
        return RELEASE_BACKUP_NAME.format(
            backup_dir=BACKUP_DIR,
            dt=datetime.datetime.now().strftime("%d.%m.%Y.%H.%M"),
            db_name=self.database_name
        )


def run_management_command(some_command, env):
    with lcd(env.project_directory):
        cmd = "{0}/bin/python manage.py {1}".format(
            env.virtual_env_path, some_command
        )
        print(cmd)
        result = local(cmd, capture=True)
        print(result.stdout)
        print(result.stderr)
    if result.failed:
        raise ValueError(
            "{} failed".format(cmd)
        )
    return result


def pip_create_virtual_env(virtual_env_path, remove_existing, python_path=None):
    print("Creating new environment")
    if remove_existing:
        local("rm -rf {}".format(virtual_env_path))
    else:
        if os.path.isdir(virtual_env_path):
            raise ValueError(
                "Directory {} already exists".format(virtual_env_path)
            )

    if python_path:
        cmd = "/usr/bin/virtualenv -p {} {}".format(
            python_path, virtual_env_path
        )
    else:
        cmd = "/usr/bin/virtualenv {}".format(virtual_env_path)
    local(cmd)


@task
def pip_create_deployment_env(branch_name):
    print("Creating deployment environment")
    new_env = Env(branch_name)
    pip_create_virtual_env(
        new_env.deployment_env_path, remove_existing=True
    )
    pip = "{}/bin/pip".format(new_env.deployment_env_path)
    local("{0} install pip==9.0.1".format(pip))
    local("{0} install -r requirements-deployment.txt".format(pip))



def pip_install_requirements(new_env):
    print("Installing requirements")

    pip = "{}/bin/pip".format(new_env.virtual_env_path)
    local("{0} install pip==18.0".format(pip))

    # get's us round the connection pool
    # from
    # https://github.com/pypa/pip/issues/1805
    local("{0} install requests==2.20.1".format(pip))
    local("{0} install -r requirements.txt".format(pip))


def pip_set_project_directory(some_env):
    print("Setting the project directory")
    local("echo '{0}' > {1}/.project".format(
        some_env.project_directory, some_env.virtual_env_path
    ))


def postgres_command(command):
    return local(
        '{0} "{1}"'.format(DB_COMMAND_PREFIX, command),
    )


# def postgres_create_database(some_env, remove_existing):
#     """ creates a database and user if they don't already exist.
#         the db_name is created from the release name
#     """
#     print("Creating the database")

#     select_result = local(
#         "sudo -u postgres psql -tAc \"SELECT 1 FROM pg_database \
# WHERE datname='{}'\"".format(some_env.database_name),
#         capture=True
#     )
#     database_exists = "1" in select_result.stdout
#     print(select_result.stderr)
#     print(select_result.stdout)

#     if database_exists:
#         if remove_existing:
#             postgres_command(
#                 "DROP DATABASE {0}".format(some_env.database_name)
#             )
#         else:
#             raise ValueError('database {} already exists'.format(
#                 some_env.database_name
#             ))

#     postgres_command("CREATE DATABASE {0}".format(some_env.database_name))
#     postgres_command("GRANT ALL PRIVILEGES ON DATABASE {0} TO {1}".format(
#         some_env.database_name, DB_USER
#     ))


def postgres_load_database(backup_name, new_env):
    """
    !!!
    !!!
    IMPORTANT: This is the command to roll back to a release backup database
    !!!
    !!!
    """
    print("Loading the database {}".format(new_env.database_name))
    local("cat {0} | gunzip | sudo -u postgres psql -d {1}".format(
        backup_name,
        new_env.database_name
    ))


def services_symlink_nginx(new_env):
    print("Symlinking nginx")
    abs_address = "{}/etc/nginx.conf".format(new_env.project_directory, "")
    if not os.path.isfile(abs_address):
        raise ValueError(
            "we expect an nginx conf to exist at {}".format(abs_address)
        )

    symlink_name = '/etc/nginx/sites-enabled/{}'.format(MODULE_NAME)

    # In case we have trailing enabled elcid configs.
    # TODO >=2.6  remove this, just remove the one above
    names = [symlink_name, symlink_name+'-rfh']
    for name in names:
        if os.path.islink(name):
            local("sudo rm {}".format(name))

    local('sudo ln -s {0} {1}'.format(abs_address, symlink_name))


def services_create_celery_conf(new_env):
    print("Creating celery conf")
    template = jinja_env.get_template(
        'etc/conf_templates/celery.conf.jinja2'
    )
    output = template.render(
        env_name=new_env.virtual_env_path,
        log_dir=LOG_DIR
    )
    celery_conf = '{0}/etc/celery.conf'.format(
        new_env.project_directory
    )

    if os.path.isfile(celery_conf) and not new_env.remove_existing:
        raise ValueError(
            'celery conf {} unexpectedly already exists'.format(
                celery_conf
            )
        )

    local("rm -f {}".format(celery_conf))

    with open(celery_conf, 'w') as f:
        f.write(output)


def services_symlink_upstart(new_env):
    print("Symlinking upstart")
    abs_address = "{}/etc/upstart.conf".format(new_env.project_directory, "")
    if not os.path.isfile(abs_address):
        raise ValueError(
            "we expect an upstart conf to exist {}".format(abs_address)
        )
    symlink_name = '/etc/init/{}.conf'.format(PROJECT_NAME)
    local("sudo rm -f {}".format(symlink_name))

    local('sudo ln -s {0} {1}'.format(
        abs_address,
        symlink_name
    ))

def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join([
        random.SystemRandom().choice(chars) for i in range(50)
    ])

def services_create_local_settings(new_env, additional_settings):
    print("Creating local settings")
    new_settings = copy.copy(additional_settings)
    new_settings["db_name"] = new_env.database_name
    new_settings["db_user"] = DB_USER
    new_settings["secret_key"] = generate_secret_key()
    template = jinja_env.get_template(
        'etc/conf_templates/local_settings.py.jinja2'
    )
    output = template.render(new_settings)
    local_settings_file = '{0}/{1}/local_settings.py'.format(
        new_env.project_directory, MODULE_NAME
    )

    if os.path.isfile(local_settings_file) and not new_env.remove_existing:
        raise ValueError(
            "local settings file {} already exists".format(
                local_settings_file
            )
        )
    local("rm -f {}".format(local_settings_file))

    with open(local_settings_file, 'w') as f:
        f.write(output)


def services_create_gunicorn_conf(new_env):
    print("Creating gunicorn conf")
    template = jinja_env.get_template(
        'etc/conf_templates/gunicorn.conf.jinja2'
    )
    output = template.render(
        env_name=new_env.virtual_env_path
    )
    gunicorn_conf = '{0}/etc/gunicorn.conf'.format(
        new_env.project_directory
    )

    if os.path.isfile(gunicorn_conf) and not new_env.remove_existing:
        raise ValueError(
            'gunicorn conf {} unexpectedly already exists'.format(
                gunicorn_conf
            )
        )

    local("rm -f {}".format(gunicorn_conf))

    with open(gunicorn_conf, 'w') as f:
        f.write(output)


def services_create_upstart_conf(new_env):
    print("Creating upstart conf")
    template = jinja_env.get_template('etc/conf_templates/upstart.conf.jinja2')
    output = template.render(env=new_env)
    upstart_conf = '{0}/etc/upstart.conf'.format(
        new_env.project_directory
    )

    if os.path.isfile(upstart_conf) and not new_env.remove_existing:
        raise ValueError(
            'gunicorn conf {} unexpectedly already exists'.format(
                upstart_conf
            )
        )

    local("rm -f {}".format(upstart_conf))

    with open(upstart_conf, 'w') as f:
        f.write(output)


def restart_supervisord(new_env):
    print("Restarting supervisord")
    # warn only in case nothing is running
    # don't restart supervisorctl as we need to be running the correct
    # supervisord
    local("{0}/bin/supervisord -c {1}/etc/production.conf".format(
        new_env.deployment_env_path, new_env.project_directory
    ))


def restart_nginx():
    print("Restarting nginx")
    local('sudo service nginx restart')


def write_cron_backup(new_env):
    """
    Creates a cron job that copies a file to a remote server

    This is not like other cron jobs as it does not run on test
    """
    print("Writing cron {}_backup".format(PROJECT_NAME))
    template = jinja_env.get_template('etc/conf_templates/cron_backup.jinja2')
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.deployment_env_path,
        branch=new_env.branch,
        unix_user=UNIX_USER
    )
    cron_file = "/etc/cron.d/{0}_backup".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_lab_tests(new_env):
    """
    Creates a cron job that runs the 'batch_load2' management command
    """
    print("Writing cron {}_batch_test_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_lab_tests.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    local("echo '{0}' | sudo tee {1}".format(
        output, CRON_TEST_LOAD
    ))

def write_cron_lab_pre_load(new_env):
    """
    Creates a cron job that runs the lab pre-loader
    """
    print("Writing cron {}_lab_pre_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_lab_pre_load.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_lab_pre_load".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))

def write_cron_sync_demographics(new_env):
    """
    Creates a cron job that syncs demographics
    """
    print("Writing cron {}_sync_demographics".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_sync_demographics.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_sync_demographics".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_covid(new_env):
    """
    Creates a cron job that performs covid specific tasks
    """
    print("Writing cron {}_classify_covid".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_covid.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_covid".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_icu_load(new_env):
    """
    Creates a cron job that runs the ICU Handover loader
    """
    print("Writing cron {}_icu_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_icu_load.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_icu_load".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))

def write_cron_tb_patient_load(new_env):
    """
    Creates a cron job that creates tb patients/episodes
    if they have tb appointments
    """
    print("Writing cron {}_tb_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_tb_patient_load.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_tb_patient_load".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_admission_load(new_env):
    """
    Creates a cron job that runs the admission loader
    """
    print("Writing cron {}_admission_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_admission_load.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_admission_load".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_intrahospital_api(new_env):
    """
    Creates a cron job that runs intrahospital_api jobs
    """
    print("Writing cron {}_intrahospital_api".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_intrahospital_api.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_intrahospital_api".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_appointment_load(new_env):
    """
    Creates a cron job that runs the appointment loader
    """
    print("Writing cron {}_appointment_load".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_appointment_load.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_appointment_load".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))




def write_cron_icu_refresh(new_env):
    """
    Creates a cron job that runs the ICU hard refresh
    """
    print("Writing cron {}_hard_refresh".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_icu_hard_refresh.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_icu_hard_refresh".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_disk_check(new_env):
    """
    Creates a cron job that checks our disk space
    """
    print("Writing cron {}_disk_space".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_disk_checker.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_check_disk_space".format(PROJECT_NAME)
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_backup_size(new_env):
    """
    Creates a cron job that stores the size of today's backup
    """
    print("Writing cron {}_backup_size".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_backup_size.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    local("echo '{0}' | sudo tee {1}".format(
        output, "/etc/cron.d/elcid_backup_size"
    ))


def write_cron_load_amt_handover(new_env):
    """
    Creates a cron job that loads the AMT handover list
    """
    print("Writing cron {}_sync_amt_handover".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_sync_amt_handover.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_sync_amt_handover".format(
        PROJECT_NAME
    )
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def write_cron_calculte_amt_dashboard(new_env):
    """
    Creates a cron job that calculates the AMT dashboard
    """
    print("Writing cron {}_calculate_amt_dashboard".format(PROJECT_NAME))
    template = jinja_env.get_template(
        'etc/conf_templates/cron_calculate_amt_dashboard.jinja2'
    )
    fabfile = os.path.abspath(__file__).rstrip("c")  # pycs won't cut it
    output = template.render(
        fabric_file=fabfile,
        virtualenv=new_env.virtual_env_path,
        unix_user=UNIX_USER,
        project_dir=new_env.project_directory
    )
    cron_file = "/etc/cron.d/{0}_calculate_amt_dashboard".format(
        PROJECT_NAME
    )
    local("echo '{0}' | sudo tee {1}".format(
        output, cron_file
    ))


def send_error_email(error, some_env):
    print("Sending error email")
    run_management_command(
        "error_emailer '{}'".format(
            error
        ),
        some_env
    )


def clean_old_backups():
    now = datetime.datetime.now()
    dates = []
    for i in xrange(3):
        dates.append(
            (now - datetime.timedelta(i)).strftime(BACKUP_DT_FORMAT)
        )
    for f in os.listdir(BACKUP_DIR):
        if f.startswith("back"):
            if f.endswith("sql") or f.endswith("sql.gz"):
                if not any(i for i in dates if i in f):
                    os.remove(os.path.join(BACKUP_DIR, f))


def copy_backup(current_env):
    private_settings = get_private_settings()
    string_args = {}
    string_args["backup_storage_address"]   = private_settings["backup_storage_address"]
    string_args["backup_storage_password"]  = private_settings["backup_storage_password"]
    string_args["backup_storage_username"]  = private_settings["backup_storage_username"]
    string_args["backup_storage_directory"] = private_settings["backup_storage_directory"]
    string_args["backup_storage_ip"]        = private_settings["backup_storage_ip"]
    string_args["dump_location"]            = current_env.backup_name
    string_args["dump_name"]                = current_env.backup_file_name
    cmd = "smbclient '{backup_storage_address}' {backup_storage_password} -U {backup_storage_username} -I {backup_storage_ip} -D {backup_storage_directory} -c 'put {dump_location} {dump_name}'"
    cmd = cmd.format(**string_args)

    if not os.path.isfile(current_env.backup_name):
        send_error_email(
            "unable to find backup {}".format(
                current_env.backup_name
            ),
            current_env
        )
    else:
        with settings(warn_only=True):
            failed = local(cmd).failed

        if failed:
            send_error_email(
                "unable to copy backup {}".format(
                    current_env.backup_name,
                ),
                current_env
            )


def get_private_settings():
    if not os.path.isfile(PRIVATE_SETTINGS):
        raise ValueError(
            "unable to find additional settings at {}".format(
                PRIVATE_SETTINGS
            )
        )

    with open(PRIVATE_SETTINGS) as privado:
        result = json.load(privado)
        err_template = "we require '{}' in your private settings"

        required_fields = [
            "db_password",
            "additional_settings",  # required even if its just an empty dict

            # the details of the network drive we putting the backups on
            "backup_storage_address",
            "backup_storage_password",
            "backup_storage_username",
            "backup_storage_directory",
        ]
        for field in required_fields:
            if field not in result:
                raise ValueError(err_template.format(field))

        if not result["backup_storage_address"].startswith("\\"):
            e = "We expect the backup storage address to be a network drive address"
            raise ValueError(e)
    return result


@task
def clone_branch(branch_name):
    branch_env = Env(branch_name)
    if os.path.isdir(branch_env.project_directory):
        raise ValueError("{} already exists".format(
            branch_env.project_directory
        ))

    print("Cloning into {}".format(branch_env.project_directory))

    local(
        "git clone -b {0} {1} {2}".format(
            branch_name,
            GIT_URL,
            branch_env.project_directory
        )
    )


def diff_status(old_status_json, new_status_json):
    old_status = json.loads(old_status_json)
    new_status = json.loads(new_status_json)

    for time_period in ["all_time", "last_week"]:
        flawed = False
        print("looking at {}".format(time_period))
        new_time_period = new_status[time_period]
        old_time_period = old_status[time_period]
        missing = list(
            set(new_time_period.keys()) - set(old_time_period.keys())
        )

        for m in missing:
            flawed = True
            print("missing {} from old".format(m))

        for k, v in old_time_period.items():
            if k not in new_time_period:
                flawed = True
                print("missing {} from new".format(k))
            else:
                new_result = new_time_period[k]
                if not v == new_result:
                    flawed = True
                    print(
                        "for {} we used to have {} but now have {}".format(
                            k, v, new_result
                        )
                    )
        if not flawed:
            print("no difference")


@task
def create_private_settings():
    if os.path.isfile(PRIVATE_SETTINGS):
        raise ValueError(
            'private settings already exist at {}'.format(PRIVATE_SETTINGS)
        )
    with open(PRIVATE_SETTINGS, "w") as privado:
        json.dump(
            dict(
                db_password="",
                host_string="",
                backup_storage_address="",
                backup_storage_username="",
                backup_storage_password="",
                backup_storage_directory="",
                additional_settings={}
            ),
            privado,
            indent=4
        )


def get_python_3():
    return local("which python3.6", capture=True)

def infer_current_branch():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_beginning = Env('').project_directory

    if not current_dir.startswith(project_beginning):
        er_temp = 'we are in {0} but expect to be in a directory beginning \
with {1}'
        raise ValueError(er_temp.format(current_dir, project_beginning))
    return current_dir.replace(project_beginning, "")


def validate_private_settings():
    private_settings = get_private_settings()
    if "host_string" not in private_settings:
        raise ValueError(
            'we need a host string inorder to scp data to a backup server'
        )

    if "backup_storage_password" not in private_settings:
        raise ValueError(
            'we need the password of the backup server inorder to scp data to \
a backup server'
        )

def _roll_back(branch_name):
    roll_to_env = Env(branch_name)
    # symlink the nginx conf
    services_symlink_nginx(roll_to_env)

    # symlink the upstart conf
    services_symlink_upstart(roll_to_env)

    restart_supervisord(roll_to_env)
    restart_nginx()


@task
def roll_back_test(branch_name):
    _roll_back(branch_name)


@task
def roll_back_prod(branch_name):
    validate_private_settings()

    roll_to_env = Env(branch_name)
    _roll_back(branch_name)
    create_pg_pass(roll_to_env, get_private_settings())
    write_cron_backup(roll_to_env)
    write_cron_lab_tests(roll_to_env)

### def create_pg_pass(env, additional_settings):
###     pg_pass = os.path.join(os.environ["HOME"], ".pgpass")

###     print("Creating pg pass")
###     template = jinja_env.get_template(
###         'etc/conf_templates/pgpass.conf.jinja2'
###     )
###     output = template.render(
###         db_name=env.database_name,
###         db_user=DB_USER,
###         db_password=additional_settings["db_password"]
###     )

###     with open(pg_pass, 'w') as f:
###         f.write(output)

###     os.chmod(pg_pass, stat.S_IRWXU)


@task
def dump_and_copy(branch_name):
    env = Env(branch_name)
    try:
        dump_database(env, env.database_name, env.backup_name)
        copy_backup(env)
        clean_old_backups()
    except Exception as e:
        send_error_email(
            "database backup failed with '{}'".format(str(e)), env
        )


def dump_database(env, db_name, backup_name):
    pg = "pg_dump {db_name} -U {db_user} | gzip > {bu_name}"
    local(
        pg.format(
            db_name=db_name,
            db_user=DB_USER,
            bu_name=backup_name
        )
    )


@task
def deploy_prod(old_branch, old_database_name=None):
    """
    Occassionally (for instance, when transitioning to new deployment
    scripts) we will change the database naming scheme
    We have an optional old_database_name for transitory deployments
    where we need to pass it in rather than infer from the branch
    name as normal.
    """
    new_branch = infer_current_branch()
    old_env = Env(old_branch)
    new_env = Env(new_branch)
    backup_name = old_env.release_backup_name

    validate_private_settings()

    if old_database_name is None:
        dbname = old_env.database_name
    else:
        dbname = old_database_name

    dump_database(old_env, dbname, backup_name)

    old_status = run_management_command("status_report", old_env)

    if backup_name and not os.path.isfile(backup_name):
        raise ValueError("unable to find backup {}".format(backup_name))

    # local("sudo rm /etc/cron.d/elcid*") # We have to move them out as it takes too long to do post backup.

    # the new env that is going to be live
    new_env = Env(new_branch)

    # the private settings
    private_settings = get_private_settings()
    env.host_string = private_settings["host_string"]

    with settings(warn_only=True):
        local("sudo pkill super; pkill gunic; pkill celery;")

    # Setup environment
    pip_create_virtual_env(
        new_env.virtual_env_path,
        False,
        python_path=get_python_3()
    )
    pip_set_project_directory(new_env)
    pip_create_deployment_env(new_branch)

    pip_install_requirements(new_env)

    # create a database
#    postgres_create_database(new_env, False)     This adds hours to the deployment time
#    create_pg_pass(new_env, private_settings)    We don't really need to do this

    # load in a backup
    # if backup_name:
    #     postgres_load_database(backup_name, new_env) # Takes hours, requires a huge free disk to have many copies

    postgres_command("ALTER DATABASE {old} RENAME TO {new};".format(
        old=old_env.database_name,
        new=new_env.database_name
    ))

    # create the local settings used by the django app
    services_create_local_settings(new_env, private_settings)

    services_create_gunicorn_conf(new_env)
    services_create_upstart_conf(new_env)

    # symlink the nginx conf
    services_symlink_nginx(new_env)

    # symlink the upstart conf
#    services_symlink_upstart(new_env)

    # symlink the celery conf
    services_create_celery_conf(new_env)

    # django setup
    run_management_command("collectstatic --noinput", new_env)
    run_management_command("migrate --noinput", new_env)
    run_management_command("create_singletons", new_env)
    run_management_command("load_lookup_lists", new_env)
    restart_supervisord(new_env)
    restart_nginx()

    # Cron jobs
    write_cron_lab_tests(new_env)
    write_cron_lab_pre_load(new_env)

    write_cron_sync_demographics(new_env)

    write_cron_icu_load(new_env)
    write_cron_icu_refresh(new_env)
    write_cron_tb_patient_load(new_env)
    write_cron_intrahospital_api(new_env)
    write_cron_appointment_load(new_env)

    write_cron_admission_load(new_env)
    write_cron_disk_check(new_env)
    write_cron_backup_size(new_env)

    write_cron_covid(new_env)

    write_cron_load_amt_handover(new_env)
    write_cron_calculte_amt_dashboard(new_env)

    write_cron_backup(new_env)
    new_status = run_management_command("status_report", new_env)

    diff_status(new_status, old_status)
