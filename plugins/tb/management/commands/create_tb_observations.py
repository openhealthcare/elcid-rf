"""
A management command that looks at TB Appointments
and TB lab tests in the last 72 hours and creates a TB Patient
object.
"""
import datetime
import time
from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand
from plugins.labtests.models import Observation
from plugins.tb import logger, episode_categories, models
from opal.models import Patient


TB_OBSERVATIONS = [models.TBPCR, models.AFBSmear, models.AFBCulture, models.AFBRefLib]


@transaction.atomic
def populate_tests(since):
    labtests_obs_qs = Observation.objects.filter(last_updated__gte=since)

    for tb_obs_model in TB_OBSERVATIONS:
        labtests_tb_obs_qs = labtests_obs_qs.filter(
            test__test_name__in=tb_obs_model.TEST_NAMES,
        ).filter(observation_name=tb_obs_model.OBSERVATION_NAME)
        # delete existing
        tb_obs_model.objects.filter(observation__in=labtests_tb_obs_qs).delete()

        new_instances = []
        for obs in labtests_tb_obs_qs:
            new_instances.append(tb_obs_model.populate_from_observation(obs))
        tb_obs_model.objects.bulk_create(new_instances)
        logger.info(
            f"Creating TB observations: created {len(new_instances)} {tb_obs_model.OBSERVATION_NAME}"
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        three_days_ago = timezone.now() - datetime.timedelta(3)
        start = time.time()
        populate_tests(three_days_ago)
        end_populate = time.time()
        logger.info(
            f"Creating TB observations: Finished creating TB tests in {end_populate-start}s"
        )
        patient_ids = set()
        for tb_obs_model in TB_OBSERVATIONS:
            patient_ids = patient_ids.union(
                tb_obs_model.objects.filter(positive=True)
                .values_list("patient_id", flat=True)
                .distinct()
            )
        need_tb_episodes = Patient.objects.exclude(
            episode__category_name=episode_categories.TbEpisode.display_name
        ).filter(id__in=patient_ids)
        for need_tb_episode in need_tb_episodes:
            need_tb_episode.episode_set.create(
                category_name=episode_categories.TbEpisode.display_name
            )
        logger.info(
            f"Creating TB observations: Created {len(need_tb_episodes)} episodes for people with positive TB tests"
        )
        end_episode_create = time.time()
        logger.info(
            f"Creating TB observations: Finished creating TB episodes {end_episode_create-end_populate}s"
        )
