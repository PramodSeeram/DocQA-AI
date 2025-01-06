from django.test import TestCase
from .models import UploadedDocument

class UploadedDocumentTest(TestCase):
    def test_document_upload(self):
        doc = UploadedDocument.objects.create(file='test.xlsx')
        self.assertEqual(str(doc.file), 'test.xlsx')
