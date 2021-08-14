from unittest import mock

from django.test import TestCase

from documents.models import Document


class DocumentQuerySetTestCase(TestCase):
    def setUp(self) -> None:
        self.doc1 = Document.objects.create(title='doc1')
        self.doc2 = Document.objects.create(title='doc2')
        self.doc3 = Document.objects.create(title='doc3')

    def test_document_query_set_delete(self):
        mock_file_delete = mock.Mock()
        mock_delete = mock.Mock()
        with mock.patch('django.db.models.fields.files.FieldFile.delete', mock_file_delete):
            with mock.patch('django.db.models.QuerySet.delete', mock_delete):
                Document.objects.all().delete()
        self.assertEqual(mock_delete.call_count, 1)
        self.assertEqual(mock_file_delete.call_count, 3)

    def test_document_representation(self):
        self.assertEqual(self.doc1.__str__(), f'{self.doc1.id} {self.doc1.title}')

