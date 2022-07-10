from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.models import Model
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.test import TestCase

from documents.views import DocumentUpload


class DocumentUploadTestCase(TestCase):
    def test_document_upload_without_model(self):
        document = DocumentUpload()
        with self.assertRaises(ImproperlyConfigured):
            document.get_object()

    def test_document_upload_without_field(self):
        document = DocumentUpload()
        document.model = Model
        document.form_class = Form
        with self.assertRaises(AttributeError):
            document.form_valid(form=mock.Mock())

    def test_document_upload_raise_integrity_error(self):
        document = DocumentUpload()
        document.model = Model
        document.form_class = Form
        document.success_url = reverse("home")
        document.get_object = mock.Mock(side_effect=IntegrityError())
        ret = document.form_valid(form=mock.Mock())
        self.assertIsInstance(ret, HttpResponseRedirect)
