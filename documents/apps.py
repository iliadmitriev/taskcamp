from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentConfig(AppConfig):
    name = "documents"
    verbose_name = _("Documents")
