from unittest import mock

from django.test import TestCase

from documents.forms import DocumentModelForm


class DocumentModelFormTestCase(TestCase):
    def setUp(self) -> None:
        self.model_form = DocumentModelForm()
        self.save_mock = mock.Mock()

    def test_document_model_form_save(self):
        with mock.patch('django.forms.ModelForm.save', self.save_mock):
            self.model_form.save(commit=True)
            self.save_mock.assert_called_once()

    def test_document_model_form_not_save(self):
        with mock.patch('django.forms.ModelForm.save', self.save_mock):
            self.model_form.save(commit=False)
            self.save_mock.assert_called_once()
