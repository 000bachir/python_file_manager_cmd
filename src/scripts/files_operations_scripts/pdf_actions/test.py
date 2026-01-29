import os
import pymupdf
from pathlib import Path


def spliting_single_pages():
    try:
        filename = "./testing.pdf"
        file = Path(filename)
        if not file.exists:
            print("error the file doesn't not exist \n")
            return False
        if not file.is_file:
            print("error the provided item is not a file \n")
            return False

        # init of an empty output pdf file
        src = pymupdf.open(file)
        doc = pymupdf.open()

        for spage in src:
            r = spage.rect
            d = pymupdf.Rect(spage.cropbox_position, spage.cropbox_position)
            r1 = r / 2
            r2 = r1 + (r1.width, 0, r1.width, 0)
            r3 = r1 + (0, r1.height, 0, r1.height)
            r4 = pymupdf.Rect(r1.br, r.br)

            rect_list = [r1, r2, r3, r4]
            for rx in rect_list:
                rx += d
                page = doc.new_page(-1, width=rx.width, height=rx.height)
                page.show_pdf_page(page.rect, src, spage.number, clip=rx)

                doc.save("poster-" + src.name, garbage=3, deflate=True)

    except Exception as e:
        print(f"error something went wrong : {e}\n")
        raise


spliting_single_pages()
