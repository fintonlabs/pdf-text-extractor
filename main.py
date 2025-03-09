import os
import re
import json
import pandas as pd
from PyPDF2 import PdfFileReader
from typing import List, Dict, Union


class PDFProcessor:
    """
    A class used to process PDF files in a directory.

    ...

    Attributes
    ----------
    dir_path : str
        a string representing the directory path where the PDF files are located

    Methods
    -------
    get_pdf_files():
        Returns a list of PDF files in the directory.
    extract_text(file_path: str) -> Dict[int, str]:
        Extracts text from a PDF file and returns a dictionary where keys are page numbers and values are extracted text.
    search_text(search_string: str) -> Dict[str, List[int]]:
        Searches for a string in all PDF files and returns a dictionary where keys are file names and values are page numbers where the string is found.
    export_text(file_path: str, format: str):
        Exports the extracted text to a specified format (TXT, CSV, JSON).
    """

    def __init__(self, dir_path: str):
        """
        Constructs all the necessary attributes for the PDFProcessor object.

        Parameters
        ----------
            dir_path : str
                directory path where the PDF files are located
        """

        if not os.path.isdir(dir_path):
            raise FileNotFoundError(f"The directory {dir_path} does not exist.")
        self.dir_path = dir_path

    def get_pdf_files(self) -> List[str]:
        """Returns a list of PDF files in the directory."""

        return [file for file in os.listdir(self.dir_path) if file.endswith('.pdf')]

    def extract_text(self, file_path: str) -> Dict[int, str]:
        """
        Extracts text from a PDF file.

        Parameters
        ----------
            file_path : str
                path to the PDF file

        Returns
        -------
            dict
                a dictionary where keys are page numbers and values are extracted text
        """

        try:
            with open(file_path, 'rb') as file:
                pdf = PdfFileReader(file)
                return {i: pdf.getPage(i).extractText() for i in range(pdf.getNumPages())}
        except Exception as e:
            print(f"An error occurred while processing the file {file_path}: {str(e)}")
            return {}

    def search_text(self, search_string: str) -> Dict[str, List[int]]:
        """
        Searches for a string in all PDF files.

        Parameters
        ----------
            search_string : str
                string to search for

        Returns
        -------
            dict
                a dictionary where keys are file names and values are page numbers where the string is found
        """

        result = {}
        for file in self.get_pdf_files():
            file_path = os.path.join(self.dir_path, file)
            text = self.extract_text(file_path)
            for page, content in text.items():
                if re.search(search_string, content):
                    if file in result:
                        result[file].append(page)
                    else:
                        result[file] = [page]
        return result

    def export_text(self, file_path: str, format: str):
        """
        Exports the extracted text to a specified format (TXT, CSV, JSON).

        Parameters
        ----------
            file_path : str
                path to the PDF file
            format : str
                format to export the text to (TXT, CSV, JSON)
        """

        text = self.extract_text(file_path)
        if format.lower() == 'txt':
            with open(f"{file_path}.txt", 'w') as file:
                for page, content in text.items():
                    file.write(f"Page {page}:\n{content}\n")
        elif format.lower() == 'csv':
            df = pd.DataFrame.from_dict(text, orient='index', columns=['Text'])
            df.to_csv(f"{file_path}.csv")
        elif format.lower() == 'json':
            with open(f"{file_path}.json", 'w') as file:
                json.dump(text, file)
        else:
            raise ValueError(f"Invalid format {format}. Please choose from TXT, CSV, JSON.")


# Example usage
processor = PDFProcessor('/path/to/directory')
print(processor.get_pdf_files())
print(processor.extract_text('/path/to/file.pdf'))
print(processor.search_text('search string'))
processor.export_text('/path/to/file.pdf', 'txt')