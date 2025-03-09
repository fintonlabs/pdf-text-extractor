import os
import unittest
from pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = PDFProcessor('/path/to/directory')

    def test_get_pdf_files(self):
        files = self.processor.get_pdf_files()
        self.assertTrue(all(file.endswith('.pdf') for file in files))

    def test_extract_text(self):
        text = self.processor.extract_text('/path/to/file.pdf')
        self.assertIsInstance(text, dict)
        self.assertTrue(all(isinstance(key, int) and isinstance(value, str) for key, value in text.items()))

    def test_search_text(self):
        result = self.processor.search_text('search string')
        self.assertIsInstance(result, dict)
        self.assertTrue(all(isinstance(key, str) and isinstance(value, list) for key, value in result.items()))

    def test_export_text(self):
        self.processor.export_text('/path/to/file.pdf', 'txt')
        self.assertTrue(os.path.isfile('/path/to/file.pdf.txt'))

if __name__ == '__main__':
    unittest.main()