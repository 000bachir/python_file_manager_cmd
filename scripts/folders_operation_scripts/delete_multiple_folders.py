

#! important note need when the user has selected i need to display it's content before the deletion happend i think of a loop and also maybe if it a nested folders let him see what is inside of one of each still need to check if i have the conpetence 


import os 
from pathlib import Path
import shutil
from typing import Optional, List

class FolderHandler():
    def __init__(self):
        self.validate_response = ["delete_tree", "exit"]

    def get_user_input(self, prompt: str, validate_options: Optional[List[str]]) -> Optional[str]:
        while True:
            response = input(prompt).strip().lower()
            if response in validate_options:
                return response
            print(f"Please enter one of the following options: {', '.join(validate_options)}")

    def get_validate_source_directory(self) -> Optional[str]:
        directory_path = Path(input("Please, enter the directory where the files or folders are located to process them: "))
        if not directory_path.exists():
            print(f"Error: the directory path provided is wrong: {directory_path}")
            return None
        if not directory_path.is_dir():
            print("Error: the path is not a valid directory")
            return None
        return str(directory_path)
    
    def get_files_and_folder_in_directory_path(self, directory_path: str):
        try:
            path = Path(directory_path)
            items = list(path.iterdir())
            if not items:
                print("Error: there are no files or folders here.")
                return []
            print(f"\nItems in folder {directory_path}")
            for index, item in enumerate(items, 1):
                print(f"{index}. {item.name}")
            return [str(item) for item in items]
        except Exception as e:
            print(f"Error, denied access to the directory: {e}")
            return []
        
    def get_valid_file_indices(self, max_index: int) -> List[int]:
        if max_index == 0:
            print("Sorry, empty folder nothing to index")
            return []
        while True:
            indices_input = input("\nEnter the file numbers to process (comma-separated, e.g., 1,3): ")
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

class DeletingNestedFolders():

    def list_folders_inside_of_a_given_directory(self , directory_path:str) :

        path = Path(directory_path)
        folders = [f for f in path.iterdir() if f.is_dir()]

        if not folders :
            print("no folders in this directory")
            return []
        
        for index , folder in enumerate(folders , 1) :
            print(f"{index} - {folder.name}")
        return folders
    

    def list_contents_of_selected_folder(self , folder_path:str) :
        print(f"\nContents of folder: {folder_path}")

        try :
            items = list(Path(folder_path))
            if not items :
                print("error, the folder is empty")
            else :
                for item in items :
                    print(f"-{item.name}")
        except Exception as e :
            print("error rading the folder")

    def deleting_tree_folder(self, path: str, folder_list: List[str]):
        for folder in folder_list:
            # Use the full path from folder_list directly since get_files_and_folder_in_directory_path returns full paths
            if not os.path.exists(folder):
                print(f"Path does not exist: {folder}")
                continue
            try:
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
                    print(f"Deleted folder and its contents: '{folder}'")
                else:
                    os.remove(folder)
                    print(f"Deleted file: '{folder}'")
            except PermissionError:
                print(f"Access denied: Cannot delete '{folder}'")
            except Exception as e:
                print(f'An error occurred while deleting "{folder}": {e}')

def main():
    print("Welcome user")
    dir_manager = FolderHandler()
    deleter = DeletingNestedFolders()

    while True:
        action = dir_manager.get_user_input("Enter 'delete_tree' to remove a folder or 'exit' to quit: ", dir_manager.validate_response)
        if action == "exit":
            print("Thank you for using the folder deletion utility. Goodbye!")
            break
        elif action == "delete_tree":
            # Get valid source directory
            source_dir = None
            while source_dir is None:
                source_dir = dir_manager.get_validate_source_directory()
                if source_dir is None:
                    retry = input("Try again with another directory? (yes/no): ").strip().lower()
                    if retry != "yes":
                        print("Operation Canceled")
                        break
            
            # If we got a valid directory, proceed with deletion
            if source_dir:
                folders_list = deleter.list_contents_of_selected_folder(source_dir)
                if not folders_list:
                    print("No items available to select for deletion in this directory.")
                else:
                    folders_indices = dir_manager.get_valid_file_indices(len(folders_list))
                    if folders_indices:  # Only proceed if the user selected items
                        selected_folders = [folders_list[i] for i in folders_indices]
                        consent = input("This action is quite destructive. Are you sure you want to proceed? (yes/no): ").strip().lower()
                        if consent == "no":
                            print("Operation canceled.")
                        elif consent == "yes":
                            deleter.deleting_tree_folder(source_dir, selected_folders)
                            print("Operation was successful.")
                    else:
                        print("No items selected for deletion.") 

if __name__ == "__main__":
    main()

