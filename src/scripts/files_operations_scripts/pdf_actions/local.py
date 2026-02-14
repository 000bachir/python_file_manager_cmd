import pymupdf as pdf
from datetime import date, datetime, timezone
from pprint import pprint, pformat
import json


def extract_metadata():
    document = "./عقد تمهين سريدي محمد بشير.pdf"
    try:
        pdf_document = pdf.open(document)
        if not pdf_document:
            print("ERROR : no pdf document was provided\n")
            return False
        if pdf_document is not None:
            meta = pdf_document.metadata
            if meta is not None:
                meta = meta.copy()
            else:
                meta = {}
            meta["title"] = meta.get("title") or "unknown title"
            meta["author"] = meta.get("author") or "unknown author"
            meta["subject"] = meta.get("subject") or "unknown subject"
            meta["keywords"] = meta.get("keywords") or "tag1, tag2"
            meta["producer"] = meta.get("producer") or "PDFium"
            # format the date if not found
            now_utc = datetime.now(timezone.utc).strftime("D:%Y%m%d%H%M%SZ")
            meta["creationDate"] = f"({now_utc})" or meta.get("creationDate")

            meta["modDate"] = meta.get("modDate") or "no info"
            pdf_document.set_metadata(meta)
            print(json.dumps(pdf_document.metadata, indent=4))
    except Exception as e:
        print(f"error {e}")


extract_metadata()
