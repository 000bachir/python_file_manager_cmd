from re import A
from PIL import Image
import pymupdf


def create_pdf_from_images(list_images=None):

    A4_height = 842
    A4_Width = 595

    list_images = [
        "./sample_data/image01.jpg",
        "./sample_data/image02.jpg",
        "./sample_data/image03.jpg",
    ]
    if not list_images:
        print("no images have been found")

    try:
        doc = pymupdf.open()
        for image in list_images:
            img = Image.open(image)
            if not img:
                print("could not open the image")
                return
            img_width, img_height = img.size

            page = doc.new_page(width=A4_Width, height=A4_height)

            scale = min(A4_Width / img_width, A4_height / img_height)

            new_width = img_width * scale
            new_height = img_height * scale
            rect = pymupdf.Rect(
                                (A4_Width - new_width) / 2,      # x0
                                (A4_height - new_height) / 2,    # y0  ← bottom position
                                (A4_Width + new_width) / 2,      # x1
                                (A4_height + new_height) / 2     # y1
            page.insert_image(rect, filename=image)
        doc.save("output.pdf")
        doc.close()

    except Exception as e:
        print(f"Error : {e}")


create_pdf_from_images()
