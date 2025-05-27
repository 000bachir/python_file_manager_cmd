import os
from typing import List, Optional, Dict
from datetime import datetime
import shutil
import re
from pathlib import Path


class FileRenamingUtility:
    def __init__(self):
        self.valid_responses = {"yes", "no"}  # Using set for O(1) lookups
        
    def get_user_input(self, prompt: str, valid_options: Optional[set] = None) -> str:
        """Get and validate user input."""
        while True:
            response = input(prompt).strip().lower()
            if valid_options is None or response in valid_options:
                return response
            print(f"Please enter one of the following options: {', '.join(valid_options)}")

    def get_valid_directory(self) -> Optional[str]:
        """Get and validate directory path from user."""
        directory_path = input("Please enter the path where the files are located: ").strip()
        if not os.path.exists(directory_path):
            print("Error: Directory does not exist.")
            return None
        if not os.path.isdir(directory_path):
            print("Error: Path is not a directory.")
            return None
        return directory_path

    def get_files_in_directory(self, directory_path: str) -> List[str]:
        """Get list of files in directory and display them."""
        try:
            files = os.listdir(directory_path)
            if not files:
                print("The directory is empty.")
                return []
            
            print("\nFiles and folders:")
            for index, file in enumerate(files, 1):
                print(f"{index}. {file}")
            return files
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return []

    def get_valid_file_indices(self, max_index: int) -> List[int]:
        """Get and validate file indices from user."""
        while True:
            indices_input = input("\nEnter the file numbers to rename (comma-separated, e.g., 1,3): ")
            try:
                indices = [
                    int(i.strip()) - 1 
                    for i in indices_input.split(",") 
                    if i.strip().isdigit()
                ]
                
                # Validate indices are in range
                invalid_indices = [i + 1 for i in indices if i < 0 or i >= max_index]
                if invalid_indices:
                    print(f"Invalid selection(s): {invalid_indices}. Please try again.")
                    continue
                    
                return indices
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

    def validate_filename(self, filename: str) -> bool:
        """Validate if filename is legal."""
        invalid_chars = '<>:"/\\|?*'
        return (
            filename 
            and not any(char in filename for char in invalid_chars)
            and not filename.startswith(".")
        )

    def rename_files(self, directory_path: str, files: List[str], indices: List[int]) -> bool:
        """Rename selected files with error handling."""
        success = True
        for index in indices:
            old_name = files[index]
            old_path = os.path.join(directory_path, old_name)
            
            while True:
                new_name = input(f"Enter new name for '{old_name}' (including extension): ").strip()
                if not self.validate_filename(new_name):
                    print("Invalid filename. Please avoid special characters and hidden files.")
                    continue
                    
                new_path = os.path.join(directory_path, new_name)
                if os.path.exists(new_path) and new_path != old_path:
                    print(f"Error: '{new_name}' already exists. Choose a different name.")
                    continue
                    
                try:
                    os.rename(old_path, new_path)
                    print(f"Successfully renamed '{old_name}' to '{new_name}'")
                    break
                except OSError as e:
                    print(f"Error renaming '{old_name}': {e}")
                    success = False
                    break
        
        return success

    def run(self):
        """Main program loop."""
        print("Welcome to the File Renaming Utility!")
        
        while True:
            action = self.get_user_input(
                "Would you like to rename your files? (yes/no): ",
                self.valid_responses
            )
            
            if action == "no":
                print("Thank you for using the File Renaming Utility. Goodbye!")
                break
                
            directory_path = self.get_valid_directory()
            if not directory_path:
                continue
                
            files = self.get_files_in_directory(directory_path)
            if not files:
                continue
                
            indices = self.get_valid_file_indices(len(files))
            if not indices:
                print("No valid files selected.")
                continue
                
            self.rename_files(directory_path, files, indices)


class EnhancedFileRenamingUtility(FileRenamingUtility):
    def __init__(self):
        super().__init__()
        self.history: Dict[str, str] = {}  # Store rename history
        self.backup_dir = "_backups"
        
    def create_backup(self, file_path: str) -> Optional[str]:
        """Create a backup of the file before renaming."""
        try:
            backup_path = os.path.join(
                os.path.dirname(file_path),
                self.backup_dir,
                f"{os.path.basename(file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
            return None

    def batch_rename(self, directory_path: str, pattern: str, replacement: str) -> None:
        """Rename multiple files using a regex pattern."""
        files = self.get_files_in_directory(directory_path)
        renamed = 0
        
        for file in files:
            if re.search(pattern, file):
                new_name = re.sub(pattern, replacement, file)
                if self.validate_filename(new_name):
                    old_path = os.path.join(directory_path, file)
                    new_path = os.path.join(directory_path, new_name)
                    
                    if os.path.exists(new_path):
                        print(f"Skipping '{file}': '{new_name}' already exists")
                        continue
                        
                    self.create_backup(old_path)
                    try:
                        os.rename(old_path, new_path)
                        self.history[file] = new_name
                        renamed += 1
                    except OSError as e:
                        print(f"Error renaming '{file}': {e}")
                        
        print(f"Renamed {renamed} files")

    def undo_last_rename(self, directory_path: str) -> None:
        """Undo the last rename operation."""
        if not self.history:
            print("No rename operations to undo")
            return
            
        last_old_name, last_new_name = self.history.popitem()
        old_path = os.path.join(directory_path, last_new_name)
        new_path = os.path.join(directory_path, last_old_name)
        
        try:
            os.rename(old_path, new_path)
            print(f"Undid rename: '{last_new_name}' back to '{last_old_name}'")
        except OSError as e:
            print(f"Error undoing rename: {e}")

    def preview_rename(self, directory_path: str, pattern: str, replacement: str) -> None:
        """Preview the results of a batch rename operation."""
        files = self.get_files_in_directory(directory_path)
        print("\nPreview of rename operations:")
        
        for file in files:
            if re.search(pattern, file):
                new_name = re.sub(pattern, replacement, file)
                print(f"'{file}' -> '{new_name}'")

    def run(self):
        """Enhanced main program loop with more options."""
        print("Welcome to the Enhanced File Renaming Utility!")
        
        while True:
            print("\nOptions:")
            print("1. Rename individual files")
            print("2. Batch rename using pattern")
            print("3. Undo last rename")
            print("4. Preview batch rename")
            print("5. Exit")
            
            choice = self.get_user_input("Select an option (1-5): ", {"1", "2", "3", "4", "5"})
            
            if choice == "5":
                print("Thank you for using the Enhanced File Renaming Utility. Goodbye!")
                break
                
            directory_path = self.get_valid_directory()
            if not directory_path:
                continue

            if choice == "1":
                # Original individual file rename logic
                files = self.get_files_in_directory(directory_path)
                if not files:
                    continue
                indices = self.get_valid_file_indices(len(files))
                if not indices:
                    print("No valid files selected.")
                    continue
                self.rename_files(directory_path, files, indices)
                
            elif choice == "2":
                # Batch rename
                pattern = input("Enter search pattern (regex): ")
                replacement = input("Enter replacement pattern: ")
                self.batch_rename(directory_path, pattern, replacement)
                
            elif choice == "3":
                # Undo last rename
                self.undo_last_rename(directory_path)
                
            elif choice == "4":
                # Preview batch rename
                pattern = input("Enter search pattern (regex): ")
                replacement = input("Enter replacement pattern: ")
                self.preview_rename(directory_path, pattern, replacement)

def main():
    utility = EnhancedFileRenamingUtility()
    utility.run()

if __name__ == "__main__":
    main()