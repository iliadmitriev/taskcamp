import importlib
import sys
from unittest import mock

from django.test import TestCase

from taskcamp import urls


class UrlsTestCase(TestCase):
    def test_media_and_debug_toolbar_with_debug_on(self):
        with mock.patch("pkgutil.find_loader", mock.Mock(return_value=True)):
            with self.settings(DEBUG=True):
                sys.modules["debug_toolbar"] = mock.Mock()
                importlib.reload(urls)
                del sys.modules["debug_toolbar"]
                url_list = list(
                    map(lambda x: x.pattern.regex.pattern, urls.urlpatterns)
                )
                self.assertIn("^__debug__/", url_list)
                self.assertIn("^media/(?P<path>.*)$", url_list)
