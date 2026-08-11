"""
check if the file exist and is readable --- 
check if the file size is allowed within limits --- 
chekc the pdf magic bytes %PDF --- 
chekc if a real parser can open the file --- 


"""
import pymupdf
import logging
from pathlib import Path
class InvalidPdfFile(Exception) : 
    pass
class FileValidation():
    def __init__(self , enbale_loggin : bool) -> None:
        if enbale_loggin: 
            logging.basicConfig(
                level=logging.INFO , 
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.logger = logging.getLogger(__name__)
        self.logger.info("PDF FILE VALIDATION\n")

    def check_file_existence(self , file_path : str) : 
        path = Path(file_path)
        if not path.is_file() : 
            raise InvalidPdfFile(f"The file cannot be found\n")

    def check_file_size(self ,file_path : str , max_file_size : int = 150) : 
        path = Path(file_path)
        size = path.stat().st_size
        if size == 0 : 
            raise InvalidPdfFile("File is empty")
        elif size > max_file_size * 1024 * 1024 : 
            raise InvalidPdfFile(f"file is too big to process , max accepted {max_file_size}")
        else : 
            self.logger.info("size is accepted")

    def chekc_file_signature(self , file_path : str) : 
        path = Path(file_path)

        with path.open('rb') as f : 
            header = f.read(5)

        if header != b"%PDF-" : 
            raise InvalidPdfFile("File header are not a valid ones\n")


    def check_file_with_parser(self , file_path : str) : 
        path = Path(file_path)

        try : 
            with pymupdf.open(path) as pdf : 
                if pdf.page_count == 0 : 
                    raise InvalidPdfFile("File contains zero pages, invalid!!!\n")
                if pdf.is_encrypted : 
                    raise InvalidPdfFile("the file is encrypted ")
        except pymupdf.FileDataError as e : 
            self.logger.error("PDF is corrupted or malformed\n")
        except Exception as e : 
            raise InvalidPdfFile("Unable to read the file")



    


