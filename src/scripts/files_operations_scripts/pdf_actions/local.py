import pymupdf as pdf
from datetime import date, datetime, timezone
from pprint import pprint, pformat
import json
from tqdm import tqdm


def test_func():
    doc = pdf.open("./testing_file.pdf")
    for page in tqdm(doc, desc="converting to svg", unit="page"):
        svg_content = page.get_svg_image()
        with open(f"page_{page.number}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
    doc.close()


test_func()
