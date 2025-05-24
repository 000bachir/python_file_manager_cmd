"""  deleting a single or multiple folders with naming them and for the multiple they have to be seperated by commas  """
#! need to add removing  tree of directory with shutils : my guess is thet i check for the folder what is inside and then asking the user if he want to remove them 


import os
import shutil
from utils import Getting_valid_directory


def delete_single_folder(path, folder_name):
    full_path = os.path.join(path, folder_name)
    if not os.path.exists(full_path):
        print(f'The folder "{folder_name}" does not exist in "{path}".')
        return False
    try:
        shutil.rmtree(full_path)
        print(f'The folder "{folder_name}" has been deleted successfully.')
        return True
    except PermissionError:
        print(f'Access denied: You do not have permission to delete "{full_path}".')
    except Exception as e:
        print(f'An error occurred: {e}')
    return False

def delete_multiple_folders(path, folder_list):
    for folder in folder_list:
        folder = folder.strip()
        full_path = os.path.join(path, folder)
        if not os.path.exists(full_path):
            print(f'The folder "{folder}" does not exist in "{path}".')
        else:
            try:
                shutil.rmtree(full_path)
                print(f"Folder '{folder}' deleted from {full_path}")
            except PermissionError:
                print(f'Access denied: You do not have permission to delete "{full_path}".')
            except Exception as e:
                print(f'An error occurred while deleting "{folder}": {e}')

def get_user_input(prompt):
    return input(prompt).strip().lower()

def main():
    print("Welcome to the Folder Deletion Utility")
    
    while True:
        action = get_user_input("Would you like to delete a single folder (S), multiple folders (M), or quit (Q)? ").lower()
        
        if action == 'q':
            print("Thank you for using the Folder Deletion Utility. Goodbye!")
            break
        
        path = input("Please enter the path where the folder(s) are located: ").strip()
        
        if action == 's':
            folder_name = input("Please enter the name of the folder you want to delete: ").strip()
            delete_single_folder(path, folder_name)
        elif action == 'm':
            folder_list = input("Please enter the list of folders you want to delete, separated by commas: ").split(',')
            delete_multiple_folders(path, folder_list)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()