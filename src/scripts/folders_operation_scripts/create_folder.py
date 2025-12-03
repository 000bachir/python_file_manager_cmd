"""creating a single or multiple folders with naming them and for the multiple they have to be seperated by commas"""

import os
from typing import Optional, Union, Any
import logging


class FileCreatingUtility:
    def __init__(self, enable_loggin: bool = True):
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("file creation class starting!!!\n")
        self.valid_response = {"yes", "no"}

    def get_user_input(self, prompt: str, valid_response: Optional[set] = None) -> str:
        # Get and validate user input
        while True:
            response = input(prompt).strip().lower()
            if valid_response is None or response in valid_response:
                return response
            self.logger.info(
                f"Please enter one of the following options: {', '.join(valid_response)}\n"
            )

    def get_valid_directory(self) -> Optional[str]:
        # Get and validate directory path from user.
        directory_path = input(
            "Please enter the path where the files are located: "
        ).strip()
        if not os.path.exists(directory_path):
            self.logger.error("Error: Directory does not exist\n")
            return None
        if not os.path.isdir(directory_path):
            self.logger.error("The path is not a directory\n")
            return None
        return directory_path

    def validate_file_name(self, filename: str) -> Optional[Union[bool, Any]]:
        # Validate the file name is legal in Windows
        invalid_chars = '<>:"/\\|?*'
        return (
            filename
            and not any(char in filename for char in invalid_chars)
            and not filename.startswith(".")
        )

    def Creating_Single_Folder(self, path: str, name_folder: str) -> bool:
        full_path = os.path.join(path, name_folder)
        if os.path.exists(full_path):
            print(f'The folder "{name_folder}" already exists in "{path}".')
            return False
        try:
            os.mkdir(full_path)
            print(f'The folder "{name_folder}" has been created at: "{path}".')
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
        return False

    def Creating_multiple_folders(self, path: str, list_of_folders: list) -> None:
        success_count = 0
        for folder_name in list_of_folders:
            folder_name = folder_name.strip()
            if self.Creating_Single_Folder(path, folder_name):
                success_count += 1
        print(f"Created {success_count} out of {len(list_of_folders)} folders.")

    def run(self) -> None:
        self.logger.info("Welcome to the File Creation Utility!\n")
        while True:
            action = self.get_user_input(
                "Would you like to create folders? (yes/no): ", self.valid_response
            )
            if action == "no":
                self.logger.warning(
                    "Thank you for using the File Creation Utility. Goodbye!\n"
                )
                break

            directory_path = self.get_valid_directory()
            if not directory_path:
                continue

            folder_type = self.get_user_input(
                "Do you want to create a single folder or multiple folders? (single/multiple): ",
                {"single", "multiple"},
            )

            if folder_type == "single":
                folder_name = input(
                    "Enter the name of the folder to create: \n"
                ).strip()
                if self.validate_file_name(folder_name):
                    self.Creating_Single_Folder(directory_path, folder_name)
                else:
                    self.logger.warning("Invalid folder name\n")

            elif folder_type == "multiple":
                folder_names = input("Enter folder names separated by commas: ").split(
                    ","
                )
                valid_folder_names = [
                    name
                    for name in folder_names
                    if self.validate_file_name(name.strip())
                ]
                if valid_folder_names:
                    self.Creating_multiple_folders(directory_path, valid_folder_names)
                else:
                    self.logger.warning("No valid folder names were entered\n")


def main():
    utility = FileCreatingUtility()
    utility.run()


if __name__ == "__main__":
    main()

