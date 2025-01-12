from pdf_extractor import extract_from_pdf_pages

pdf_file_path = "pdf_data/2022BC_NYC_BuildingCodes_Definitions.pdf"

def run():
    pages = extract_from_pdf_pages(pdf_file_path)
    print(type(pages))
    print(pages[0])
    print(len(pages))


if(__name__ == "__main__"):
    run()
    