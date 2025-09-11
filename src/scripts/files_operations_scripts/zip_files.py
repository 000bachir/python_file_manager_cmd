
# gather qll of the files into a zip file 



import os 
from typing import Optional , List
import zipfile
from zipfile import ZipFile

import os
import zipfile
from typing import List, Optional


class CombiningFilesIntoZipFormat:
    def __init__(self) -> None:
        self.validate_response = {"yes", "no"}

    def get_user_input(self, prompt: str, validate_options: Optional[set] = None) -> str:
        while True:
            response = input(prompt).strip().lower()
            if validate_options is None or response in validate_options:
                return response
            print(f"Please enter one of the following options: {', '.join(validate_options)}")

    def get_valide_working_directory(self):
        directory_path = input("Please, enter the directory where the files are located to merge them into a zip file: ")
        if not os.path.exists(directory_path):
            print(f"Error: The directory path provided is wrong: {directory_path}")
            return None
        if not os.path.isdir(directory_path):
            print("Error: The path is not a valid directory")
            return None
        return directory_path

    def get_files_in_directory(self, directory_path: str) -> List[str]:
        """Display the files in the given directory."""
        try:
            files = os.listdir(directory_path)
            if not files:
                print(f"Error: There are no files in this directory: {directory_path}")
                return []
            print("\nFiles in the folder:")
            for index, file in enumerate(files, 1):
                print(f"{index}. {file}")
            return files
        except Exception as error:
            print(f"Error accessing directory: {error}")
            return []

    def get_valide_indices(self, max_index: int) -> List[int]:
        """Get valid file indices."""
        while True:
            indices_input = input("\nEnter the file numbers to copy (comma-separated, e.g., 1,3): ")
            try:
                indices = [
                    int(i.strip()) - 1 for i in indices_input.split(",")
                    if i.strip().isdigit()
                ]

                invalid_indices = [
                    i + 1 for i in indices
                    if i < 0 or i >= max_index
                ]

                if invalid_indices:
                    print(f"Invalid selection(s): {invalid_indices}. Please try again.")
                    continue
                return indices
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

    def zip_files(self , directory_path : str , files : List[str] , indices:List[int] , zip_output_path : str) : 
        """
        Zips selected files in a directory into a ZIP archive.
    Args:
        directory_path: The path to the directory containing the files.
        files: The list of files in the directory.
        indices: The indices of the files to be zipped.
        zip_output_path: The full path to the ZIP file to be created.
    """
        try : 
            output_directory = input("Enter the path to the directory where the ZIP file should be created: ").strip().lower()
            if not os.path.exists(output_directory) :
                print(f"Error: The specified output directory does not exist: {output_directory}")
            #!defining te final zipfile path 
            zip_output_path = os.path.join(output_directory , zip_output_path)

            with zipfile.ZipFile(zip_output_path , "w" , zipfile.ZIP_DEFLATED) as zip_file :
                for index in indices :
                    file_name = files[index]
                    file_path = os.path.join(directory_path , file_name)
                    if os.path.isfile(file_path) : #?skip directories
                        zip_file.write(file_path, arcname=file_name)
                print(f"Files successfully zipped into {zip_output_path}")

        except Exception as e :
            print(f"Error creating ZIP file: {e}")




    def run(self):
        print("Welcome to the File Compressing Utility!")
        while True:
            action = self.get_user_input(
                "Would you like to compress your files? (yes/no): ", self.validate_response
            )

            if action == "no":
                print("Thank you for using the File Compressing Utility. Goodbye!")
                break

            if action == "yes":
                directory_path = self.get_valide_working_directory()
                if not directory_path:
                    continue

                files = self.get_files_in_directory(directory_path)
                if not files:
                    continue

                indices = self.get_valide_indices(len(files))
                if not indices:
                    continue

                zip_output_path = input("Enter the name of the ZIP file to create (e.g., output.zip): ").strip()
                self.zip_files(directory_path, files, indices, zip_output_path)


def main():
    utility = CombiningFilesIntoZipFormat()
    utility.run()


if __name__ == '__main__':
    main()
