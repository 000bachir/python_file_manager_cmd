"""
this will check if a file a file is a valid pdf file by looking at the file signature
"""
import logging
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError
class PdfUtilsClass : 
    def __init__(self , enable_loggin : bool )-> None : 
        if enable_loggin : 
            logging.basicConfig(
                level=logging.INFO , 
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.logger = logging.getLogger(__name__)
        self.logger.info("PDF UTILS CLASS CREATED\n")
    def valid_pdf(self , filename: str) -> bool:
        try:
            with open(filename, "rb") as f:
                header = f.read(4)
                if header == b"%PDF":
                    self.logger.info("valid pdf file")
                    return True
                else:
                    self.logger.error("invalid pdf file")
                    return False
        except FileNotFoundError:
            print(f"error file not found : {filename}")
            return False
        except Exception as e:
            print(f"validation function crashed, check error : {e}")
            return False
    def check_file_size(self , target_file) : 
        if not target_file : 
            self.logger.error(f"No {target_file} found \n")
            return
        try : 
            file_size_bytes = Path(target_file).stat().st_size
        except Exception as e : 
            self.logger.error(f"ERROR could not check the file size : {e}")
            return None
        units = ["b" , "kb" , "mb" , "gb"]
        size = float(file_size_bytes)
        for unit in units : 
            if size < 1024 or size == units[-1] : 
                return f"{size:.2f} {unit}"
            size /= 1024
    def check_file_metadata(self , target_file) : 
        try :
            with open(target_file, "rb") as file :
                pdf_file = PdfReader(file)
                pdf_file_infos = pdf_file.metadata
                if pdf_file_infos :
                    self.logger.info("PDF file possess metadata \n")
                    return True
                else : 
                    self.logger.warning("PDF file do not contain metadata\n")
                    return False
        except FileNotFoundError as error :
            self.logger.error(f"Error could not open and find the file {error}")
            return False
    def is_pdf_corrupted(self , file) -> bool : 
        if not self.check_file_metadata(file) : 
            return False
        try : 
            file_reader = PdfReader(file)
            pages_length = len(file_reader.pages)
            if pages_length == 0 : 
                self.logger.warning("file do not seem correct")
                return False
            return True
        except PdfReadError as e : 
            self.logger.error(f"File appears to be corrupted : {e} \n")
            return True
    def check_file_protection(self , target_file) : 
    



    











