

#! just a reminder that there is a library called PyMuPDF that perform various actions on a pdf file 


from docx2pdf import convert
import os 
from typing import Optional, List 
from pathlib import Path
import zipfile
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.Getting_valid_directory import GettingValidDirectory


class UserActions:
    def __init__(self):
        self.validate_response = ["convert", "exit"]



class ConvertingFiles:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_docx_file(filepath: str) -> bool:
        filepath = filepath.strip().lower()

        if not filepath.lower().endswith(".docx"):
            print(f"Not a .docx file: {filepath}")
            return False

        if not os.path.isfile(filepath):
            print(f"File does not exist: {filepath}")
            return False

        try:
            with zipfile.ZipFile(filepath, 'r') as z:
                return '[Content_Types].xml' in z.namelist()
        except Exception as e:
            print(f"Invalid DOCX structure or corrupted file: {filepath}\nError: {e}")
            return False

    @staticmethod
    def convert_files_to_pdfs(selected_files: List[str], output_dir: str):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        converted_count = 0
        error_count = 0

        print(f"\nConverting {len(selected_files)} files...")

        for file_path in selected_files:
            file_path = Path(file_path)

            if not file_path.is_file():
                print(f"❌ Cannot convert {file_path.name}: not a valid file.")
                error_count += 1
                continue

            # Check if it's a DOCX file
            if not ConvertingFiles.is_valid_docx_file(str(file_path)):
                print(f"❌ Skipping {file_path.name}: not a valid DOCX file.")
                error_count += 1
                continue

            try:
                # Keep same name, just change extension to .pdf
                output_file = output_dir / (file_path.stem + ".pdf")

                # Avoid overwrite by adding suffix if needed
                counter = 1
                while output_file.exists():
                    output_file = output_dir / f"{file_path.stem}_{counter}.pdf"
                    counter += 1

                convert(str(file_path), str(output_file))
                print(f"✅ Converted: {file_path.name} → {output_file.name}")
                converted_count += 1

            except Exception as e:
                print(f"❌ Error converting {file_path.name}: {e}")
                error_count += 1

        print(f"\nSummary: {converted_count} converted, {error_count} errors.\n")

def main():
    user_actions = UserActions()
    dir_manager = GettingValidDirectory()
    converter = ConvertingFiles()

    while True:
        action = dir_manager.get_user_prompt(
            "Enter 'convert' to convert DOCX files to PDF or 'exit' to quit: ",
            user_actions.validate_response 
        )

        if action == "exit":
            print("Thank you for using the DOCX to PDF converter. Goodbye!")
            break

        elif action == 'convert':
            # Get valid source directory
            source_dir = None
            while source_dir is None:
                source_dir = dir_manager.get_valid_directory()
                if source_dir is None:
                    retry = input("Try again with another directory? (yes/no): ").strip().lower()
                    if retry != "yes":
                        print("Operation canceled")
                        break
            
            if source_dir:
                files_list = dir_manager.list_files_and_folders(source_dir)
                if not files_list:
                    print("No files available to convert in this directory.")
                else:
                    file_indices = dir_manager.get_valid_files_indices(len(files_list))
                    if file_indices:
                        selected_files = [files_list[i] for i in file_indices]
                        
                        print(f"\nSelected files:")
                        for file_path in selected_files:
                            file_path = Path(file_path)
                            file_type = "📁 Directory" if file_path.is_dir() else "📄 File"
                            print(f"- {file_type}: {file_path.name}")
                        
                        # Get output directory
                        print(f"\nOutput directory options:")
                        print("1. Same as source directory")
                        print("2. Choose different directory")
                        
                        output_choice = input("Enter choice (1 or 2): ").strip()
                        
                        if output_choice == "1":
                            output_dir = source_dir
                        elif output_choice == "2":
                            output_dir = dir_manager.get_valid_directory()
                            if output_dir is None:
                                print("Invalid output directory. Using source directory.")
                                output_dir = source_dir
                        else:
                            print("Invalid choice. Using source directory.")
                            output_dir = source_dir
                        
                        consent = input(f"\nProceed with converting these files to: {output_dir}? (yes/no): ").strip().lower()
                        if consent == "yes":
                            converter.convert_files_to_pdfs(selected_files, output_dir)
                        else:
                            print("Operation canceled.")
                    else:
                        print("No files selected for conversion.")

if __name__ == "__main__":
    main()