import fitz # pdf parsing, data extraction, analysis
from fitz import Page
import os
from collections import defaultdict
import re
from typing import Tuple, List


def extract_from_pdf_pages(file_path) -> dict:
    """
    Returns the txts from the pdf document by pages.
    Each page number is a key in the returned dictionary,
    The corresopnding page texts are the value of the page
    """

    cwd = os.getcwd() # get the current running py file directory

    file_full_path = os.path.join(cwd, file_path)
    print("the pdf file path: ", file_full_path)

    doc = fitz.open(file_full_path)
    pages = defaultdict(str)

    for page_num in range(len(doc)):
        cur_page = doc.load_page(page_num)
        cur_text = cur_page.get_text()
        pages[page_num] = cur_text
    
    return pages

def extra_headings_subheadings(pdf_pages: dict) -> Tuple[List[str], List[str]]:
    """
    Returns the headings and subheadings arrays from the given pdf pages.
    """
    headings = []
    subheadings = []

    for page in pdf_pages:
        cur_page_txt = pdf_pages[page]
        cur_txt = cur_page_txt

        # use regex to extract headdings and subheadings
        heading_pattern = r"^\d+\.\s.*$"
        subheading_pattern = r"^\d+\.\d+\.\s.*$"

        heading_matches = re.findall(heading_pattern, cur_txt, re.MULTILINE)
        subheading_matches = re.findall(subheading_pattern, cur_txt, re.MULTILINE)

        headings.extend(heading_matches)
        subheadings.extend(subheading_matches)

    return headings, subheadings