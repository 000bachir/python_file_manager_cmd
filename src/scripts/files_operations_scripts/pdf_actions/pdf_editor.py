from __future__ import annotations
import logging
from pathlib import Path
import signal
import sys
import time
import pymupdf
from typing import List
from src.scripts.files_operations_scripts.organize_files import FolderNavigation
from utils.pdf_utils_function.valid_pdf import valid_pdf

"""
1️⃣ PDFEditor

Handles operations that modify existing PDFs

Examples:

split === done

merge

rotate

reorder

watermark

redact

optimize
"""


shutdown_request: bool = False


class UserActions:
    def __init__(self) -> None:
        self.validate_response = ["create", "split"]


class pdfEditor:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("pdfActions class is has started \n")
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        self.name = "PDF EDITOR"

        signal.signal(
            signal.SIGTERM, lambda signum, frame: self._handle_shutdown(signum, frame)
        )
        signal.signal(
            signal.SIGINT, lambda signum, frame: self._handle_shutdown(signum, frame)
        )

    def _handle_shutdown(self, signum, frame):
        global shutdown_request
        shutdown_request = True
        self.logger.warning(
            f"\n[{self.name}] Shutdown signal received (signal {signum}). Cleaning up..."
        )

    def _cleanup(self):
        self.logger.info(f"[{self.name}] Releasing resources...")
        time.sleep(1)  # Simulate cleanup work
        print(f"[{self.name}] Resources released.")

    def start(self):
        global shutdown_request
        self.running = True
        print(f"[{self.name}] Started. Press Ctrl+C to stop.\n")
        try:
            while self.running and not shutdown_request:
                print(
                    f"[{self.name}] Working... (shutdown_requested={shutdown_request})"
                )
                time.sleep(2)
        except Exception as e:
            self.logger.error(f"ERROR could not start the graceful shutdown : {e}")
            raise
        finally:
            # finally block guarantees cleanup runs even on unexpected exits
            self._cleanup()
            print(f"[{self.name}] Shutdown complete.")
            sys.exit(0)

    def spliting_single_pages(self, filename: str):
        if not filename:
            self.logger.warning("warning no pdf file has been provided\n")
            return False
        try:
            path_file_to_pdf = Path(filename)
            if not path_file_to_pdf.exists():
                self.logger.error("file not found\n")
                return False
            pdf_document = pymupdf.open(path_file_to_pdf)
            empty_output_pdf_file = pymupdf.open()
            for spage in pdf_document:
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
                    page.show_pdf_page(page.rect, pdf_document, spage.number, clip=rx)

        except Exception as e:
            self.logger.error(
                f"the spliting_single_pages function has crashed please check error : {e}\n"
            )
            raise


def main():
    print("Welcome user!!!\n")
    dir_manager = FolderNavigation()
    pdf_editor = pdfEditor()

    while True:
        actions = dir_manager.get_user_prompt(
            """
                Enter one of the following operation you want to procced with
                Merge\n 
                Re-arrange\n 
                Split\n 
                Rotate\n 
                Watermark\n 
                Redact\n 
                optimize\n
                or quit if you wanna exit 
            """,
            dir_manager.validate_response,
        )
        if actions == "quit":
            print("THANK YOU for using our prodect\n")
            break
