from __future__ import annotations
import logging
from pathlib import Path
import pymupdf


class UserActions:
    def __init__(self) -> None:
        self.validate_response = ["create", "split"]


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
            new_page = docs.new_page(0, height=842, width=595)
            docs.save(filename)
        except Exception as e:
            self.logger.error(
                f"the create_blank_pdf_page has crashed please see error {e}\n"
            )
            raise

    def spliting_single_pages(self, filename: str):
        filename = "./testing.pdf"
        try:
            path_file_to_pdf = Path(filename)
            if not path_file_to_pdf.exists():
                self.logger.error("file not found\n")
                return False
            intended_pdf = pymupdf.open(path_file_to_pdf)
            empty_output_pdf_file = pymupdf.open()
            for spage in intended_pdf:
                r = spage.rect
                d = pymupdf.Rect(spage.cropbox_position, spage.cropbox_position)

                r1 = r / 2
                r2 = r1 + (r1.width, 0, r1.width, 0)
                r3 = r1 + (0, r1.height, 0, r1.height)
                r4 = pymupdf.Rect(r1.br, r.br)
                rect_list = [r1, r2, r3, r4]

                for rx in rect_list:
                    rx += d
                    page = empty_output_pdf_file.new_page(
                        -1, width=rx.width, height=rx.height
                    )
                    page.show_pdf_page(page.rect, intended_pdf, spage.number, clip=rx)

        except Exception as e:
            self.logger.error(
                f"the spliting_single_pages function has crashed please check error : {e}\n"
            )
            raise
