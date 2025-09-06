


#! the script mostly works but there is a catch of where the prompt where the user enter the path to delete the folder repeats it self eed to be fixed


import os
import shutil
from typing import Optional, List
from utils import Getting_valid_directory  # Importing the module

class DeletingSingleFolderClass:
    def __init__(self):
        self.validate_response = {"delete", "exit"}
        # Call the actual class inside the module
        self.Get_Valid_Directory = Getting_valid_directory.GettingValidDirectory()
    
    def DeletingSingleFolder(self, path: str, folder_name: str) -> bool:
        full_path = os.path.join(path, folder_name)
        if not os.path.exists(full_path):
            print(f'The folder "{folder_name}" was not found in the path: {path}')
            return False
        
        try:
            shutil.rmtree(full_path)
            print(f'The folder "{folder_name}" has been deleted successfully.')
            return True
        except PermissionError:
            print(f'Access denied: unable to delete "{full_path}".')
        except Exception as e:
            print(f'An error occurred while deleting: {e}')
        return False
   
def main():
    print("Welcome to the folder deletion utility!")
    deleter = DeletingSingleFolderClass()
    dir_manager = Getting_valid_directory.GettingValidDirectory()   
    while True:
        action = dir_manager.get_user_input("Enter 'delete' to remove a folder or 'exit' to quit: ")
        if action == "exit":
            print("Thank you for using the folder deletion utility. Goodbye!")
            break
        elif action == "delete":
            path = input("Please enter the path where the folders are located: ").strip()

            while True :
                source_dir = dir_manager.get_valid_source_directory()
                if source_dir :
                    break
                retry = input("Try again with another directory? (yes/no): ")
                if retry.strip().lower() != "yes" :
                    print("Operation cancelled.")
                    break
            
            #getting the folders : 
            files = dir_manager.get_files_in_directory_path(path)
            if not files : 
                print("No files to process. Exiting.")
                break
            selected_indices = dir_manager.get_valid_file_indices(len(files))
            selected_files = [files[i] for i in selected_indices]
            for files in selected_files:
                deleter.DeletingSingleFolder(path, files)
        else:
            print("Invalid option. Please enter 'delete' or 'exit'.")

if __name__ == '__main__':
    main()
