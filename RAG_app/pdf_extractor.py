import fitz
import os
from collections import defaultdict

"""
Returns the txts from the pdf document by pages.
Each page number is a key in the returned dictionary,
The corresopnding page texts are the value of the page
"""
def extract_from_pdf_pages(file_path):

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