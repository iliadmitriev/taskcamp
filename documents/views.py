"""
Documents views module.
"""

import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from documents.forms import DocumentModelForm
from documents.models import Document

logger = logging.getLogger(__name__)


class DocumentUpload(PermissionRequiredMixin, FormView):
    """Documents upload view.

    Usage:
        1) Override in subclasses which will be use as many-to-many model.
        2) set attributes `model` and `model_field`
    """

    template_name = "document_form.html"
    permission_required = "documents.add_document"
    permission_denied_message = _("You don't have permission to upload documents.")
    form_class = DocumentModelForm
    model = None
    model_field = "documents"

    def get_object(self) -> Document:
        """Get object for editing."""
        if self.model is None:
            raise ImproperlyConfigured(
                "No object to connect document to. Provide a model attribute "
                "with many to many field documents to Documents"
            )

        obj_id = self.kwargs.get("pk")
        return get_object_or_404(self.model, pk=obj_id)

    def form_valid(self, form: DocumentModelForm) -> HttpResponseRedirect:
        """Validate form data and save to DB, redirect to success url."""
        form.save(commit=True)

        try:
            obj = self.get_object()
            documents = getattr(obj, self.model_field)
            documents.add(form.instance)
        except IntegrityError as e:
            logger.warning(f"Document upload failed due to integrity error: {e}")
            pass
        except AttributeError as e:
            logger.error(f"Document upload failed due to missing model_field: {e}")
            raise

        return HttpResponseRedirect(self.get_success_url())
