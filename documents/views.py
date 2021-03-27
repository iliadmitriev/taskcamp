from django.http import HttpResponseRedirect
from django.views.generic import FormView
from documents.forms import DocumentModeForm


class DocumentUpload(FormView):
    template_name = 'document_form.html'
    form_class = DocumentModeForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())



