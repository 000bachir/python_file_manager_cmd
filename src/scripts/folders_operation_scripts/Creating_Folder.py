"""  creating a single or multiple folders with naming them and for the multiple they have to be seperated by commas  """

import os
from typing import Optional

class FileCreatingUtility: 
    def __init__(self):
        self.valid_response = {"yes", "no"}
    
    def get_user_input(self, prompt: str, valid_response: Optional[set] = None) -> str:
        # Get and validate user input
        while True:
            response = input(prompt).strip().lower()
            if valid_response is None or response in valid_response:
                return response
            print(f"Please enter one of the following options: {', '.join(valid_response)}")

    def get_valid_directory(self) -> Optional[str]:
        # Get and validate directory path from user.
        directory_path = input("Please enter the path where the files are located: ").strip()
        if not os.path.exists(directory_path):
            print("Error: Directory does not exist.")
            return None
        if not os.path.isdir(directory_path):
            print("Error: Path is not a directory.")
            return None
        return directory_path

    def validate_file_name(self, filename: str) -> bool:
        # Validate the file name is legal in Windows
        invalid_chars = '<>:"/\\|?*'
        return (
            filename
            and not any(char in filename for char in invalid_chars)
            and not filename.startswith('.')
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
    
    def creating_nested_folders(self , path:str , list_of_nested_folders:list)->None :
        success_count = 0
        for nested_folders in list_of_nested_folders :
            nested_folders = nested_folders.strip().lower()


    def run(self) -> None:
        print("Welcome to the File Creation Utility!")
        while True:
            action = self.get_user_input(
                "Would you like to create folders? (yes/no): ",
                self.valid_response
            )
            if action == "no":
                print("Thank you for using the File Creation Utility. Goodbye!")
                break

            directory_path = self.get_valid_directory()
            if not directory_path:
                continue

            folder_type = self.get_user_input(
                "Do you want to create a single folder or multiple folders? (single/multiple): ",
                {"single", "multiple"}
            )

            if folder_type == "single":
                folder_name = input("Enter the name of the folder to create: ").strip()
                if self.validate_file_name(folder_name):
                    self.Creating_Single_Folder(directory_path, folder_name)
                else:
                    print("Invalid folder name.")

            elif folder_type == "multiple":
                folder_names = input("Enter folder names separated by commas: ").split(',')
                valid_folder_names = [name for name in folder_names if self.validate_file_name(name.strip())]
                if valid_folder_names:
                    self.Creating_multiple_folders(directory_path, valid_folder_names)
                else:
                    print("No valid folder names were entered.")


def main():
    utility = FileCreatingUtility()
    utility.run()

if __name__ == "__main__":
    main()