from django.db import models
from django.utils.translation import gettext_lazy as _

from .helpers import document_upload_path


class DocumentQuerySet(models.QuerySet):
    """queryset for Document model.
    it's only purpose to override default delete operation.
    It deletes uploaded files associated with document instances
    when deleting instance from db.
    """

    def delete(self):
        for obj in self:
            obj.document.delete()
        return super(DocumentQuerySet, self).delete()


class Document(models.Model):

    objects = DocumentQuerySet.as_manager()

    uploaded = models.DateTimeField(
        verbose_name=_("Date and time uploaded"), auto_now_add=True
    )
    document = models.FileField(
        verbose_name=_("Document"), upload_to=document_upload_path
    )
    title = models.CharField(
        verbose_name=_("Title"), max_length=100, blank=True, null=True
    )
    description = models.TextField(
        verbose_name=_("Description"), max_length=500, blank=True, null=True
    )

    def __str__(self):
        return f"{self.id} {self.title}"

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
