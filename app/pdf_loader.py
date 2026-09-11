import pymupdf

from pathlib import Path


def extract_text_from_pdf(file_path):

    file_path = Path(file_path)

    document = pymupdf.open(
        file_path
    )

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text()

        if text.strip():

            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip()
                }
            )

    document.close()

    return pages


if __name__ == "__main__":

    pdf_path = Path(
        "knowledge/registration_requirements.pdf"
    )

    pages = extract_text_from_pdf(
        pdf_path
    )

    print(
        f"PDF: {pdf_path.name}"
    )

    print(
        f"Number of pages: {len(pages)}"
    )

    for page in pages:

        print(
            f"\n--- Page {page['page_number']} ---"
        )

        print(
            page["text"]
        )