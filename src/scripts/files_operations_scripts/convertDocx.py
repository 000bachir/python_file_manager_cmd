#! just a reminder that there is a library called PyMuPDF that perform various actions on a pdf file


from docx2pdf import convert
import os
from typing import Optional, List
from pathlib import Path
import zipfile
import sys
import logging
from docx import document
from docx.shared import Inches

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.Getting_valid_directory import GettingValidDirectory


class UserActions:
    def __init__(self):
        self.validate_response = ["convert", "exit"]


class ConvertingDocxToPdf:
    def __init__(self, enable_loggin: bool = True):
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
        self.logger = logging.getLogger(__name__)
        self.logger.info("CONVERTING FILES CLASS IS GOOD TO GO\n")

    def is_valid_docx_file(self, filepath: str) -> bool:
        try:
            filepath = filepath.strip().lower()
            if not filepath.lower().endswith(".docx"):
                self.logger.warning(f"Not a .docx file: {filepath}\n")
                return False
            if not os.path.isfile(filepath):
                self.logger.warning(f"File does not exist: {filepath}\n")
                return False
            with zipfile.ZipFile(filepath, "r") as z:
                return "[Content_Types].xml" in z.namelist()
        except Exception as e:
            self.logger.error(
                f"Invalid DOCX structure or corrupted file: {filepath} Error: {e}\n"
            )
            raise

    def convert_docx_to_pdfs(self, selected_files: List[str], output_dir: Path):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        converted_count: int = 0
        error_count: int = 0
        self.logger.info(f"\t\t\t\tConverting {len(selected_files)} files...\n")
        try:
            for file_path in selected_files:
                file_path = Path(file_path)

                if not file_path.is_file():
                    self.logger.warning(
                        f"Cannot convert {file_path.name}: not a valid file\n"
                    )
                    error_count += 1
                    continue

                # Check if it's a DOCX file
                if not self.is_valid_docx_file(str(file_path)):
                    self.logger.warning(
                        f"Skipping {file_path.name}: not a valid DOCX file\n"
                    )
                    error_count += 1
                    continue
                # Keep same name, just change extension to .pdf
                output_file = output_dir / (file_path.stem + ".pdf")

                # Avoid overwrite by adding suffix if needed
                counter = 1
                while output_file.exists():
                    output_file = output_dir / f"{file_path.stem}_{counter}.pdf"
                    counter += 1

                convert(str(file_path), str(output_file))
                self.logger.info(f"Converted: {file_path.name} → {output_file.name}\n")
                converted_count += 1
            self.logger.info(
                f"\nSummary: {converted_count} converted, {error_count} errors.\n"
            )

        except Exception as e:
            self.logger.error(f"error the function convert docx to pdf crashed : {e}\n")
            raise


"""
in a nutshell what this class is going to do is it is gonna to extract the text form a docx file
save into a plain text file 
"""


class ConvertDocxToTXT:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
        self.logger = logging.getLogger(__name__)
        self.logger.info("\t\t\t\tCONVERT TO TEXT CLASS IS READY TO GO\n")

    def is_valid_docx_file(self, filepath: str) -> bool:
        try:
            filepath = filepath.strip().lower()
            if not filepath.lower().endswith(".docx"):
                self.logger.warning(f"Not a .docx file: {filepath}\n")
                return False
            if not os.path.isfile(filepath):
                self.logger.warning(f"File does not exist: {filepath}\n")
                return False
            with zipfile.ZipFile(filepath, "r") as z:
                return "[Content_Types].xml" in z.namelist()
        except Exception as e:
            self.logger.error(
                f"Invalid DOCX structure or corrupted file: {filepath} Error: {e}\n"
            )
            raise

    def extracting_text_from_docx_file(self, inital_file: str, output_file):
        Check_extension = self.is_valid_docx_file(inital_file)


# def main():
#     user_actions = UserActions()
#     dir_manager = GettingValidDirectory()
#     converter = ConvertingFile()
#
#     while True:
#         action = dir_manager.get_user_prompt(
#             "Enter 'convert' to convert DOCX files to PDF or 'exit' to quit: ",
#             user_actions.validate_response,
#         )
#
#         if action == "exit":
#             print("Thank you for using the DOCX to PDF converter. Goodbye!")
#             break
#
#         elif action == "convert":
#             # Get valid source directory
#             source_dir = None
#             while source_dir is None:
#                 source_dir = dir_manager.get_valid_directory()
#                 if source_dir is None:
#                     retry = (
#                         input("Try again with another directory? (yes/no): ")
#                         .strip()
#                         .lower()
#                     )
#                     if retry != "yes":
#                         print("Operation canceled")
#                         break
#
#             if source_dir:
#                 files_list = dir_manager.list_files_and_folders(source_dir)
#                 if not files_list:
#                     print("No files available to convert in this directory.")
#                 else:
#                     file_indices = dir_manager.get_valid_files_indices(len(files_list))
#                     if file_indices:
#                         selected_files = [files_list[i] for i in file_indices]
#                         print("\nSelected files:")
#                         for file_path in selected_files:
#                             file_path = Path(file_path)
#                             file_type = (
#                                 "📁 Directory" if file_path.is_dir() else "📄 File"
#                             )
#                             print(f"- {file_type}: {file_path.name}")
#
#                         # Get output directory
#                         print(f"\nOutput directory options:")
#                         print("1. Same as source directory")
#                         print("2. Choose different directory")
#
#                         output_choice = input("Enter choice (1 or 2): ").strip()
#
#                         if output_choice == "1":
#                             output_dir = source_dir
#                         elif output_choice == "2":
#                             output_dir = dir_manager.get_valid_directory()
#                             if output_dir is None:
#                                 print(
#                                     "Invalid output directory. Using source directory."
#                                 )
#                                 output_dir = source_dir
#                         else:
#                             print("Invalid choice. Using source directory.")
#                             output_dir = source_dir
#
#                         consent = (
#                             input(
#                                 f"\nProceed with converting these files to: {output_dir}? (yes/no): "
#                             )
#                             .strip()
#                             .lower()
#                         )
#                         if consent == "yes":
#                             converter.convert_docx_to_pdfs(selected_files, output_dir)
#                         else:
#                             print("Operation canceled.")
#                     else:
#                         print("No files selected for conversion.")


# if __name__ == "__main__":
#     main()
