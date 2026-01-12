from __future__ import annotations
import logging
from pathlib import Path
import pymupdf
from src.scripts.utils.Getting_valid_directory import GettingValidDirectory
from pathlib import Path


class UserActions:
    def __init__(self) -> None:
        self.validate_response = ["create", "delete"]


class pdfActions:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("pdfActions class is has started \n")

    def create_blank_pdf_page(self, filename: str):
        try:
            docs = pymupdf.open()
            new_page = docs.new_page(1, height=842, width=595)
            docs.save(filename)
        except Exception as e:
            self.logger.error(
                f"the create_blank_pdf_page has crashed please see error {e}\n"
            )
            raise

    def spliting_single_pages(self, filename: str):
        try:
            path_file_to_pdf = Path(filename)
            if not path_file_to_pdf.exists():
                self.logger.error("file not found\n")
                return False
            intended_pdf = pymupdf.open(path_file_to_pdf)
            empty_output_pdf_file = pymupdf.open()

        except Exception as e:
            self.logger.error(
                f"the spliting_single_pages function has crashed please check error : {e}\n"
            )
            raise
