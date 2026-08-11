import os

import tqdm
import sys
import logging 
import psutil
"""
check if the file is a valid pdf file --- 
check the user device capacity --- 
check if the pdf file is encrypted --- 
check the pdf file size --- 


"""




class PDFOCRfile : 
    def __init__(self , enbale_loggin : bool , min_cpu_core : int = 2 , min_ram_required: int = 1 ) -> None:
        if enbale_loggin: 
            logging.basicConfig(
                level=logging.INFO , 
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.logger = logging.getLogger(__name__)
        self.logger.info("PDF ocr file class init\n")
        self.min_cpu_core = min_cpu_core
        self.min_ram_required = min_ram_required

    def check_user_ram(self) : 
        memory = psutil.virtual_memory()
        self.logger.info(f"Total RAM: {memory.total / (1024**3):.2f} GB")
        self.logger.info(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        self.logger.info(f"Used RAM: {memory.used / (1024**3):.2f} GB")

        available_ram = memory.available / (1024 ** 3)
        cpu_cores = psutil.cpu_count() or 1
        try : 
            if available_ram < self.min_ram_required: 
                self.logger.warning(f"Not enough RAM , Required : {self.min_ram_required}")
            if cpu_cores < self.min_cpu_core : 
                self.logger.warning(f"Not enough cpu core available , Required {self.min_cpu_core}")
        except RuntimeError as e : 
            print(f"Not enough ressources available {e}")
        finally :  
            self.logger.info("System meets the minimum requirenemnts\n")



            
