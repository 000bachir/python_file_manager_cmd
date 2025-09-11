
#*--- this scripts only copy what is inside of a directory into another folder this more of a simple way that beginner can see or take notes (im also a beginner) ---
#! the script is nit working i keep getting the error of the file is locked maybe later am gonna sys package
import os 
import shutil
from typing import  List
from pathlib import Path
import time 
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.Getting_valid_directory import GettingValidDirectory


class UserActions : 
    def __init__(self) -> None:
        self.valid_responses = {"yes" , "no"}    

class FileCopyingClass :
    @staticmethod
    def copying_files_to_another_directory(source_directory_path: str, destination_directory_path: str, files: List[str], indices: List[int]) -> bool:
        # Check if the source directory exists
        if not os.path.exists(source_directory_path):
            print("Source directory does not exist or mis-typed.")
            return False
        
        
        if len(os.listdir(source_directory_path)) == 0 :
            print(f"error the directory provided is empty {source_directory_path}")
            return False
        

        # Check if the destination directory exists
        if not os.path.exists(destination_directory_path):
            print("Destination directory does not exist.")
            return False
        


        # Loop through the list of indices provided
        for index in indices:
            if index < len(files):  # this ensure the index is within the bond
                file_name = files[index]  # Get the file name from the files list
                source_path = os.path.join(source_directory_path, file_name)  # Build full source file path
                print(source_path)
                destination_path = os.path.join(destination_directory_path, file_name)  # Build full destination path

                # Check if the file exists in the source directory
                if os.path.exists(source_path):
                    max_tries = 5  # Maximum number of retry attempts
                    wait_seconds = 1  # Wait time between retries (in seconds)
                    
                    # Retry loop for handling locked files
                    for attempt in range(max_tries):
                        try:
                            if not os.path.isfile(source_path) :
                                print("error the folders doesn't contain copiable files")
                                return False
                            else :
                                shutil.copy2(source_path, destination_path)  # Try copying the file
                                print(f"Copied '{file_name}' to '{destination_directory_path}' (attempt {attempt + 1})")
                                break  # Success! Exit the retry loop
                        except PermissionError as e:
                            if attempt < max_tries - 1:  # Fixed condition: < instead of <=
                                print(f"File '{file_name}' is locked. Retrying in {wait_seconds}s... (attempt {attempt + 1}/{max_tries})")
                                time.sleep(wait_seconds)  # Wait before next attempt
                            else:
                                print(f"PermissionError: Cannot copy '{file_name}' after {max_tries} attempts - it may be open in another program. {e}")
                        except Exception as e:
                            # Handle other unexpected errors - don't retry for these
                            print(f"Unexpected error while copying '{file_name}': {e}")
                            break  # Exit retry loop for non-permission errors
                else:
                    # File doesn't exist in the source directory
                    print(f"File '{file_name}' does not exist in the source directory.")
            else:
                # Index is invalid (greater than the list length)
                print(f"Index {index} is out of range for the files list.")
        
        return True

def main() : 
    print("Welcome to file copying utility!!!!")
    dir_manager = GettingValidDirectory()
    user_actions = UserActions()
    file_copier = FileCopyingClass()

    while True :
        action = dir_manager.get_user_prompt(
            "Would you like to copy your files? (yes/no): ",
            user_actions.valid_responses
        )

        if action == "no" : 
            print("Thank you for using the file copier utility. Goodbye!")
            break
        
        elif action == "yes" :
            source_dir = None 
            while source_dir is None :
                source_dir = dir_manager.get_valid_directory()
                if source_dir is None :
                    retry = input("Try again with another directory? (yes/no): ").strip().lower()
                    if retry != "yes" : 
                        print("Operation canceled")
                        break
                
                if source_dir :
                    files_lists = dir_manager.list_files_and_folders(source_dir)
                    if not files_lists : 
                        print("No files available to copy in this directory.")
                    else :
                        files_indices = dir_manager.get_valid_files_indices(len(files_lists))
                        if files_indices :
                            selected_files = [files_lists[i] for i in files_indices]
                            print(f"\nSelected files:")
                            for file_path in selected_files :
                                file_path = Path(file_path)
                                file_type = "📁 Directory" if file_path.is_dir() else "📄 File"
                                print(f"- {file_type}: {file_path.name}")

                            # Get output directory
                            print(f"\nOutput directory options:")
                            print("1. Same as source directory")
                            print("2. Choose different directory")

                            output_choice = input("enter one of the choices above: (1 or 2 ): ").strip()

                            if output_choice == "1" :
                                output_dir = source_dir
                            elif output_choice == "2" :
                                output_dir = dir_manager.get_valid_directory()
                                if output_dir is None : 
                                    print("Invalid output directory. Using source directory.")
                                    output_dir = source_dir
                            else :
                                print("Invalid choice. Using source directory.")
                                output_dir = source_dir

                            consent = input(f"\nProceed with copying these files to: {output_dir}? (yes/no): ").strip().lower()

                            if consent == "yes" : 
                                file_copier.copying_files_to_another_directory(source_dir , output_dir , files_lists , files_indices)

if __name__ == "__main__" :
    main() 