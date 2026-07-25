import os
import pdfplumber
from docx import Document


def extract_pdf_text(path):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_docx_text(path):
    doc = Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def parse_document(path):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(path)

    elif extension == ".docx":
        return extract_docx_text(path)

    else:
        return ""