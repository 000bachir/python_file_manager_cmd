import logging
import pymupdf
from datetime import datetime, timezone

"""
2️⃣ PDFExtractor

Handles reading / extracting data

Examples:

extract_text

extract_images

extract_metadata

extract_annotations

page_info

"""


class pdfExtractor:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)

        self.logger.info("pdfActions class is has started \n")

    def get_pdf_metadata(self, pdf_file: str):
        if not pdf_file:
            self.logger.warning("no pdf file was provided\n")
            return False
        try:
            pdf_document = pymupdf.open(pdf_file)
            if pdf_document is not None:
                metadata = pdf_document.metadata
                if metadata is not None:
                    metadata = metadata.copy()
                else:
                    metadata = {}
                metadata["title"] = metadata.get("title") or "unknown title"
                metadata["author"] = metadata.get("author") or "unknown author"
                metadata["subject"] = metadata.get("subject") or "unknown subject"
                metadata["keywords"] = metadata.get("keywords") or "tag1, tag2"
                metadata["producer"] = metadata.get("producer") or "PDFium"
                # format the date if not found
                now_utc = datetime.now(timezone.utc).strftime("D:%Y%m%d%H%M%SZ")
                metadata["creationDate"] = f"({now_utc})" or metadata.get(
                    "creationDate"
                )
                metadata["modDate"] = metadata.get("modDate") or "no info"
                pdf_document.set_metadata(metadata)

        except Exception as e:
            self.logger.error(
                f"ERROR : the get_pdf_metadata function has crashed, check error : {e}\n"
            )
            raise
