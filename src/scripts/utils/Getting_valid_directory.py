import os 
from typing import Optional , List
from pathlib import Path

#! class for getting a valid directory


class GettingValidDirectory() :
    def __init__(self) -> None:
        pass
    
    def get_user_prompt(self, prompt: str, validate_options: List[str]) -> str:
        while True:
            response = input(prompt).strip().lower()
            if response in validate_options:
                return response
            print(f"Please enter one of the following options: {', '.join(validate_options)}")

    def get_valid_directory(self) -> Optional[str]:
        try:
            directory_path = Path(input("Please enter a valid directory path: ").strip().lower())
            if not directory_path.is_dir():
                print("Error: The path provided is not a valid directory")
                return None
            return str(directory_path)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def list_files_and_folders(self, directory_path: str) -> List[str]:
        try:
            path = Path(directory_path)
            content = list(path.iterdir())

            if not content:
                print("Error: There are no files or folders here.")
                return []
            
            print(f"\nItems in folder: {directory_path}")
            for index, item in enumerate(content, 1):
                item_type = "📁" if item.is_dir() else "📄"
                print(f"{index}. {item_type} {item.name}")
            
            return [str(item) for item in content]
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return []

    def get_valid_files_indices(self, max_index: int) -> List[int]:
        if max_index == 0:
            print("Sorry, empty folder - nothing to index")
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