from __future__ import annotations
import logging
import os
import pymupdf
from utils.pdf_utils_function.valid_pdf import valid_pdf


class fileConverter:
    def __init__(self, enable_loggin: bool) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("file converter class initiated\n")

    def convert_to_svg(self, filename: str):
        if not valid_pdf(filename):
            return False
        if valid_pdf(filename):
            doc = pymupdf.open(filename)
