from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from documents.forms import DocumentModelForm


class DocumentUpload(FormView):
    template_name = 'document_form.html'
    form_class = DocumentModelForm
    model = None
    model_field = 'documents'

    def get_object(self):
        if self.model is None:
            raise ImproperlyConfigured(
                'No object to connect document to. Provide a model '
                'with many to many field documents to Documents'
            )

        obj_id = self.kwargs.get('pk')
        obj = self.model.objects.get(pk=obj_id)

        return obj

    def form_valid(self, form):

        form.save(commit=True)

        try:
            obj = self.get_object()
            documents = getattr(obj, self.model_field)
            documents.add(form.instance)
        except IntegrityError:
            pass

        except AttributeError:
            raise AttributeError(
                f'There is no many to many field {self.model_field} '
                f'in model {self.model.__name__}\n'
                f'Perhaps you should specify model_field property'
            )

        return HttpResponseRedirect(self.get_success_url())

    def __init__(self):
        super(DocumentUpload, self).__init__()



