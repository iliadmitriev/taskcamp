"""
Documents views module.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext_lazy
from django.views.generic import FormView

from documents.forms import DocumentModelForm
from documents.models import Document


class DocumentUpload(PermissionRequiredMixin, FormView):
    """Documents upload form view.

    Usage:
        1) Override in subclasses which will be use as many-to-many model.
        2) set attributes `model` and `model_field`
    """

    template_name = "document_form.html"
    permission_required = "documents.add_document"
    permission_denied_message = gettext_lazy("You have no permission to view Projects")
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
        obj = self.model.objects.get(pk=obj_id)

        return obj

    def form_valid(self, form: DocumentModelForm) -> HttpResponse:
        """Validate form data and save to DB, redirect to success url."""
        form.save(commit=True)

        try:
            obj = self.get_object()
            documents = getattr(obj, self.model_field)
            documents.add(form.instance)
        except IntegrityError:
            pass

        except AttributeError:
            raise AttributeError(
                f"There is no many to many attribute "
                f"{self.model.__name__}.{self.model_field} "
                f"Perhaps you should specify {self.model.__name__}"
                f".model_field attribute"
            )

        return HttpResponseRedirect(self.get_success_url())

    def __init__(self) -> None:
        """Init instance."""
        super(DocumentUpload, self).__init__()
