import os 
import shutil
from typing import List
from scripts.utils.Getting_valid_directory import GettingValidDirectory


class deleting_tree_folders():
    def __init__(self):
        self.validate_response = {"delete_tree" , "exit"}
        self.Get_Valid_Directory = GettingValidDirectory()
    def delete_tree_folders(self , path:str , folder_list:List[str]) -> None :
        for folders in folder_list :
            full_path = os.path.join(path , folders)
            if not os.path.exists(full_path) :
                print(f"Path does not exist: {full_path}")
                return False
        try :
            shutil.rmtree(full_path)
            print(f"Deleted folder and its contents: '{full_path}'")

        except PermissionError :
            print(f"Access denied: Cannot delete '{full_path}'")
        except Exception as E :
            print(f'An error occurred while deleting "{folders}": {E}')
            return False
def main() :
    print("welcome user")
    deleter = deleting_tree_folders()
    dir_manager = GettingValidDirectory()

    while True :
        action = dir_manager.get_user_input("Enter 'delete_tree' to remove a folder or 'exit' to quit: ")
        if action == "exit" :
            print("Thank you for using the folder deletion utility. Goodbye!")
            break
        elif action == "delete_tree" :
           while True :
               source_dir = dir_manager.get_valid_source_directory()
               if source_dir :
                   break
               retry = input("Try again with another directory? (yes/no): ").strip().lower()
               if retry.strip().lower() != "yes" :
                   print("Operation Canceled")
                   break
               #! getting the list folders
               folders_list = dir_manager.get_files_in_directory_path(source_dir)
               if folders_list :
                   print("no folders found to delete")
                   break
               folders_indices = dir_manager.get_valid_file_indices(len(folders_list))
               selected_folders = [folders_list[i] for i in folders_indices]

               #* perform the deletion
               deleter.delete_tree_folders(source_dir , selected_folders) 
               
        else:
            print("Invalid option. Please enter 'delete' or 'exit'.")

if __name__ =="__main__" :
    main()



                







