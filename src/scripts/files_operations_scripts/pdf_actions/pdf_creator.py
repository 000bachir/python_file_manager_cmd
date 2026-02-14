from __future__ import annotations
import logging
import pymupdf

"""
3️⃣ PDFCreator

Handles creating new PDFs

Examples:

create_blank

create_from_images

create_from_text

generate_report_pdf

"""


class PDFCreator:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)

        self.logger.info("pdfActions class is has started \n")

    def create_blank_pdf_page(self, filename: str):
        if not filename:
            self.logger.warning("no pdf file has been provided\n")
            return False
        try:
            docs = pymupdf.open()
            new_page = docs.new_page(0, height=842, width=595)
            docs.save(filename)
        except Exception as e:
            self.logger.error(
                f"the create_blank_pdf_page has crashed please see error {e}\n"
            )
            raise
