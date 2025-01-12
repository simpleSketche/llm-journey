from pdf_extractor import extract_from_pdf_pages

# Tip: if the pdf you found is shown in the pdf viewer on a website,
# open the dev Element inspector, and find the html element class named / id named -> "download",
# it's hidden by default, add / change the display style property to "inline" from "hidden".
pdf_file_path = "pdf_data/2022BC_NYC_BuildingCodes_Definitions.pdf"

def run():
    pages = extract_from_pdf_pages(pdf_file_path)
    print(type(pages))
    print(pages[0])
    print(len(pages))


if(__name__ == "__main__"):
    run()
    