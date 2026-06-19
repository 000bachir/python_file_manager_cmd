import os

import tqdm
import sys
import logging 


class PDFOCRfile : 
    def __init__(self , enbale_loggin : bool ) -> None:
        if enbale_loggin: 
            logging.basicConfig(
                level=logging.INFO , 
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.logger = logging.getLogger(__name__)
        self.logger.info("PDF ocr file class init\n")
