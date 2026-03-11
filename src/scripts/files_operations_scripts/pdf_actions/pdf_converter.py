from __future__ import annotations
import logging
import os
import signal
import string
import pymupdf
from utils.pdf_utils_function.valid_pdf import valid_pdf
import tqdm
import time
import sys


# golbal shutdown variable flag
shutdown_request: bool = False


class fileConverter:
    def __init__(self, enable_loggin: bool) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("file converter class initiated\n")
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        self.name = "file converter"

        # signal handlers registers :
        signal.signal(
            signal.SIGTERM, lambda signum, frame: self._handle_shutdown(signum, frame)
        )
        signal.signal(
            signal.SIGINT, lambda signum, frame: self._handle_shutdown(signum, frame)
        )

    def _handle_shutdown(self, signum, frame):
        global shutdown_request
        shutdown_request = True
        self.running = False
        self.logger.info(
            f"\n[{self.name}] shutdown signal received (signal {signum}), Cleaning "
        )

    def _cleanup(self):
        print(f"{self.name} releasing resources")
        time.sleep(1)
        print(f"{self.name} resources released ")

    def start(self):
        global shutdown_request
        self.running = True
        self.logger.info(f"{self.name} started , press CTRL C to stop \n")
        try:
            while self.running and not shutdown_request:
                print(
                    f"[{self.name}] Working... (shutdown_requested={shutdown_request})"
                )
                time.sleep(2)
        except Exception as e:
            self.logger.error(f"ERROR : could not start, see cause : {e}")
            raise
        finally:
            self._cleanup()
            print(f"[{self.name}] Shutdown complete.")
            sys.exit(0)

    def convert_to_svg(self, filename: str):
        if not valid_pdf(filename):
            return False
        if valid_pdf(filename):
            try:
                doc = pymupdf.open(filename)
                if doc.page_count == 1:
                    page = doc[0]
                    svg_content = page.get_svg_image()
                    with open("output.svg", "w", encoding="utf-8") as f:
                        f.write(svg_content)
                    doc.close()
                if doc.page_count > 1:
                    for page in tqdm.tqdm(doc, desc="converting pages", unit="page"):
                        svg_content = page.get_svg_image()
                        with open(f"page_{page.number}", "w", encoding="utf-8") as f:
                            f.write(svg_content)
            except FileNotFoundError:
                self.logger.error("error could not find the specific file submited")
            except Exception as e:
                self.logger.error(f"errro could not convert into proper svg : {e}")
                raise
