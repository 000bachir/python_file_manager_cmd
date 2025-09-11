import os 
from pathlib import Path
from typing import Optional , List 
import re
import shutil
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.Getting_valid_directory import GettingValidDirectory


patterns = [
    # Text and Document Files
    (r".*\.(txt|md|rtf)$", "Text Files"),
    (r".*\.(doc|docx)$", "Word Documents"),
    (r".*\.(pdf)$", "PDFs"),
    (r".*\.(odt)$", "OpenDocument Text"),
    
    # Image Files
    (r".*\.(jpg|jpeg|png|gif|bmp|tiff|tif|webp)$", "Images"),
    (r".*\.(svg)$", "Vector Graphics"),
    (r".*\.(psd|xcf)$", "Image Editing Files"),
    
    # Video Files
    (r".*\.(mp4|avi|mkv|mov|wmv|flv|webm)$", "Videos"),
    
    # Audio Files
    (r".*\.(mp3|wav|flac|ogg|aac|m4a)$", "Audio"),
    
    # Spreadsheet and Data Files
    (r".*\.(xls|xlsx|ods|csv)$", "Spreadsheets"),
    (r".*\.(json|yaml|yml|xml)$", "Data Files"),
    
    # Presentation Files
    (r".*\.(ppt|pptx|odp)$", "Presentations"),
    
    # Code and Script Files
    (r".*\.(py|ipynb)$", "Python Scripts"),
    (r".*\.(js|ts|jsx|tsx)$", "JavaScript"),
    (r".*\.(html|htm|css|scss)$", "Web Files"),
    (r".*\.(java|class)$", "Java Files"),
    (r".*\.(cpp|c|h|hpp)$", "C/C++ Files"),
    (r".*\.(rb)$", "Ruby Scripts"),
    (r".*\.(sh|bash)$", "Shell Scripts"),
    
    # Archive Files
    (r".*\.(zip|rar|7z|tar|gz|bz2)$", "Archives"),
    
    # Executable and Binary Files
    (r".*\.(exe|msi|bin|app|dmg)$", "Executables"),
    
    # Database Files
    (r".*\.(sql|db|sqlite|sqlite3|mdb)$", "Databases"),
    
    # Font Files
    (r".*\.(ttf|otf|woff|woff2)$", "Fonts"),
    
    # CAD and 3D Modeling Files
    (r".*\.(dwg|dxf|stl|obj|3ds|blend)$", "CAD and 3D Models"),
    
    # Miscellaneous
    (r".*\.(iso|img)$", "Disk Images"),
    (r".*\.(log)$", "Log Files"),
    (r".*\.(bak|tmp)$", "Backup Files")
]



class FolderNavigation :
    def __init__(self):
        self.validate_response = ["arrange" , "exit"]


    def get_user_prompt(self , prompt : str , validate_options : Optional[List[str]]) -> Optional[str] :
        response = input(prompt).strip().lower()
        if response in validate_options :
            return response
        print(f"Please enter one of the following options: {', '.join(validate_options)}")

        
    def get_valid_directory(self) :
        directory_path = Path(input("please enter a valid directory path: ").strip())
        if not directory_path.is_dir() :
            print("error sorry the path provided is not a valid directory")
            return None
        return str(directory_path)
    
    def list_files_and_folders(self , directory_path : str) :
        try :
            path = Path(directory_path)
            content = list(path.iterdir())

            if not content :
                print("Error: there are no files or folders here.")
                return []
            print(f"\n Items in the folder : {directory_path}")
            for index , item in enumerate(content , 1) :
                print(f"{index}. {item.name}")
            return [str(item) for item in content]
        except Exception as e :
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

class RegroupingFiles():
    def __init__(self):
        pass

    @staticmethod
    def organize_files(directory:Path , selected_files: List[Path], patterns: List[tuple]) :
        directory = Path(directory)
        moved_count = 0
        error_count = 0
        print(f"\nOrganizing {len(selected_files)} files...")

        for file_path in selected_files :
            file_path = Path(file_path)
            if not file_path.is_file() :
                print(f"Skipping {file_path.name} (not a file)")
                continue

            moved = False

            for pattern , folder_name in patterns :
                if re.search(pattern , file_path.name , re.IGNORECASE) :
                    try :
                        target_dir = directory / folder_name
                        target_dir.mkdir(exist_ok=True)

                        target_path = target_dir / file_path.name

                        # Create full target path
                        target_path = target_dir / file_path.name
                        
                        # Handle file name conflicts
                        counter = 1
                        original_target = target_path
                        while target_path.exists():
                            stem = original_target.stem
                            suffix = original_target.suffix
                            target_path = target_dir / f"{stem}_{counter}{suffix}"
                            counter += 1
                        
                        # Move the file
                        shutil.move(str(file_path), str(target_path))
                        print(f"Moved: {file_path.name} → {folder_name}/")
                        moved_count += 1
                        moved = True
                        break
                        
                    except Exception as e:
                        print(f"Error moving {file_path.name}: {e}")
                        error_count += 1
                        break
            
                if not moved and error_count == 0:
                    print(f"No category found for: {file_path.name}")
            print(f"\nOperation completed:")
            print(f"- Files moved: {moved_count}")
            print(f"- Errors: {error_count}")

def main() :
    print("Welcome user")
    dir_manager = FolderNavigation()
    cleaner = RegroupingFiles()

    while True:
        action = dir_manager.get_user_prompt(
            "Enter 'arrange' to organize files or 'exit' to quit: ", 
            dir_manager.validate_response
        )
        
        if action == "exit":
            print("Thank you for using the file organizer. Goodbye!")
            break
            
        elif action == "arrange":
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
                    print("No files available to organize in this directory.")
                else:
                    file_indices = dir_manager.get_valid_file_indices(len(files_list))
                    if file_indices:
                        selected_files = [files_list[i] for i in file_indices]
                        
                        print(f"\nSelected files:")
                        for file_path in selected_files:
                            file_path = Path(file_path)
                            print(f"- {file_path.name}")
                        
                        consent = input("\nProceed with organizing these files? (yes/no): ").strip().lower()
                        if consent == "yes":
                            cleaner.organize_files(source_dir, selected_files, patterns)
                        else:
                            print("Operation canceled.")
                    else:
                        print("No files selected for organization.")

if __name__ == "__main__":
    main()
