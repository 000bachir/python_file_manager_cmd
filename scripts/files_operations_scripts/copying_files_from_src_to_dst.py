import os 
import shutil
from typing import Optional , List
import re
#!--- this scripts only copy what is inside of a directory into another directory ---
class CopyingDirectories : 
    def __init__(self) -> None:
        self.valid_responses = {"yes" , "no"}
    def get_user_input(self , prompt:str , valid_options:Optional[set] = None) -> str :
        """Get and validate user input."""
        while True :
            response = input(prompt).strip().lower()
            while True : 
                if valid_options is None or response in valid_options :
                    return response
                print(f"Please enter one of the following options: {', '.join(valid_options)}")


    def get_valid_source_directory(self) -> Optional[str] :
        directory_path = input("please , enter the directory where the files are located to copy them: ")
        if not os.path.exists(directory_path) :
            print(f"Error the directory path provided is wrong: {directory_path}")
            return None
        if not os.path.isdir(directory_path) :
            print("Error the path is not a valid directory")
            return None
        return directory_path 


    def get_files_in_directory_path(self , directory_path : str) -> List[str] :
        """getting the list of directories inside fo the folder"""
        try :
            files = os.listdir(directory_path)
            if not files : 
                print("error there is no files in here")
                return []
            print("\n files in folder: ")
            for index , file in enumerate(files,1) :
                print(f"{index}. {file}")
            return files
        except Exception as e :
            print(f"error accessing directory, {e}")
            return []
    
    def get_valid_file_indices(self , max_index:int) -> List[int] :
        """get and validate file indeces from user"""
        while True : 
            indices_input = input("\nEnter the file numbers to copy (comma-separated, e.g., 1,3): ")
            try : 
                indices = [
                    int(i.strip()) - 1 for i in indices_input.split(",")
                    if i.strip().isdigit()
                ]

                invalid_indices = [
                                        i + 1 for i in indices
                                        if i < 0 or i >= max_index
                                    ]
                if invalid_indices : 
                    print(f"Invalid selection(s): {invalid_indices}. Please try again.")
                    continue
                return indices
            except ValueError as e :
                print("Invalid input. Please enter valid numbers.")



    def get_valid_destination_to_copy_files(self , destination_directory_path) ->Optional[str] :
        destination_directory_path = input("Please enter the directory where the files will be located after being copied: ")
        if not os.path.exists(destination_directory_path) :
            print(f"Error: The path provided is not a directory: {destination_directory_path}")
            return None
        if not os.path.isdir(destination_directory_path) : 
            print("Error: The path entered is not a valid directory. Please try again.")
            return None
        return destination_directory_path
    
    def copying_files_to_another_directory( self,source_directory_path: str, destination_directory_path: str , files: List[str], indices: List[int]) -> bool :
        success = True
        if not os.path.exists(source_directory_path) :
            print("Source directory does not exist.")
            return None
        if not os.path.exists(destination_directory_path):
            print("Destination directory does not exist.")
            return None
        for index in indices:
            if index < len(files):
                file_name = files[index]
                source_path = os.path.join(source_directory_path, file_name)
                destination_path = os.path.join(destination_directory_path, file_name)
                
                # Check if the file exists in the source directory
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied '{file_name}' to '{destination_directory_path}'")
                else:
                    print(f"File '{file_name}' does not exist in the source directory.")
            else:
                print(f"Index {index} is out of range for the files list.")
                
    def run(self):
        """Main program loop."""
        print("Welcome to the File Renaming Utility!")
        while True:
            action = self.get_user_input(
                "Would you like to copy your files? (yes/no): ",
                self.valid_responses
            )
        
            if action == "no":
                print("Thank you for using the File Renaming Utility. Goodbye!")
                break
                
            directory_path = self.get_valid_source_directory()
            if not directory_path:
                continue
                
            files = self.get_files_in_directory_path(directory_path)
            if not files:
                continue
                
            indices = self.get_valid_file_indices(len(files))
            if not indices:
                print("No valid files selected.")
                continue

            destination = self.get_valid_destination_to_copy_files(directory_path)
            if not destination :
                continue

            self.copying_files_to_another_directory(directory_path, destination, files, indices)
            
def main() :
    utility = CopyingDirectories()
    utility.run()
if __name__ == '__main__':
    main()

