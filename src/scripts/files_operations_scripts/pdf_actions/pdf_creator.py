from __future__ import annotations
import logging
from typing import List
import PIL
import pymupdf
from PIL import Image

"""
3️⃣ PDFCreator

Handles creating new PDFs

Examples:

create_blank ---> Done 

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

    def create_pdf_from_images(self, image_list: List[str]):
        # Global variable
        A4_HEIGHT = 842
        A4_WIDTH = 595
        try:
            doc = pymupdf.open()
            for images in image_list:
                img = Image.open(images)
                if not img:
                    self.logger.error("No image could have been handeled\n")
                    return
                image_width, image_height = img.size
                page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
                scale = min(A4_WIDTH / image_width, A4_HEIGHT / image_height)
                new_width = image_width * scale
                new_height = image_height * scale

                rect = pymupdf.Rect(
                    (A4_WIDTH - new_width) / 2,  # x0
                    (A4_HEIGHT - new_height) / 2,  # y0  ← bottom position
                    (A4_WIDTH + new_width) / 2,  # x1
                    (A4_HEIGHT + new_height) / 2,  # y1
                )
                page.insert_image(rect, filename=images)
            doc.save("output.pdf")
            doc.close()

        except Exception as e:
            self.logger.error(f"Error could not create pdf file from images : {e}\n")
