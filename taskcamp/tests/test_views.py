from django.test import TestCase
from taskcamp.views import http_500


class HandlingViewsTestCase(TestCase):
    def test_500_page_handler(self):
        response = http_500(request=None)
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed('handler/500.html')
