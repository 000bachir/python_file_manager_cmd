import os
import pymupdf
from pathlib import Path
import time
from datetime import date


def pdf_parse_date_time(pdf_date_time: str):
    if not pdf_date_time:
        return
    try:
        return pymupdf.utils.get_pdf_date(pdf_date_time)
    except Exception as e:
        print(f"errro : {e}")


def extract_metadata():
    doc = pymupdf.open("./عقد تمهين سريدي محمد بشير.pdf")
    if doc.metadata is not None:
        creationDate = doc.metadata.get("creationDate")
        i_have_no_idea = date(int(creationDate))
        print(f"the creation date is : {creationDate}")
        print(type(creationDate))
        print(i_have_no_idea)


extract_metadata()
