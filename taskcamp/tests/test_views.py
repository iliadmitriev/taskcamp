from django.test import TestCase
from taskcamp.views import http_500, http_404, http_403


class HandlingViewsTestCase(TestCase):
    def test_500_page_handler(self):
        response = http_500(request=None)
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed('handler/500.html')

    def test_404_page_handler(self):
        response = http_404(request=None, exception=Exception)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('handler/404.html')

    def test_403_page_handler(self):
        response = http_403(request=None, exception=Exception)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed('handler/403.html')
