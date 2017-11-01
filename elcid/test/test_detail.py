"""
Unittests for the elCID.detail module
"""
from django.contrib.auth.models import User
from opal.core.test import OpalTestCase
from elcid import detail


class ResultViewTestCase(OpalTestCase):
    def test_slug(self):
        self.assertEqual('test_results', detail.Result.get_slug())

    @override_settings(RESULTS_VIEW=False)
    def test_invisible_without_gloss(self):
        ordinary_user = User.objects.create()
        self.assertFalse(detail.Result.visible_to(ordinary_user))

    @override_settings(RESULTS_VIEW=True)
    def test_visible_with_gloss(self):
        ordinary_user = User.objects.create()
        self.assertTrue(detail.Result.visible_to(ordinary_user))

    @override_settings(RESULTS_VIEW=False)
    def test_visible_with_superuser(self):
        self.assertTrue(detail.Result.visible_to(self.user))

    @override_settings(RESULTS_VIEW=False)
    def test_invisible_without_superuser(self):
        ordinary_user = User.objects.create()
        self.assertFalse(detail.Result.visible_to(ordinary_user))
