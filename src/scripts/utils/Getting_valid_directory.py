from typing import Any, Optional, List, Union
from pathlib import Path
import logging
#! class for getting a valid directory


class GettingValidDirectory:
    def __init__(self, enable_logging: bool = True) -> None:
        if enable_logging:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )

        self.logger = logging.getLogger(__name__)
        self.logger.info("valid directory helped is good to go \n")

    def get_user_prompt(
        self, prompt: str, validate_options: Union[List[str], Any] = None
    ) -> str:
        try:
            while True:
                response = input(prompt).strip().lower()
                if response in validate_options:
                    return response
                self.logger.info(
                    f"Please enter one of the following options: {', '.join(validate_options)}\n"
                )
        except Exception as e:
            self.logger.error(f"error getting the user prompt : {e}")
            raise

    def get_valid_directory(self) -> Optional[str]:
        try:
            directory_path = Path(
                input("Please enter a valid directory path: ").strip().lower()
            )
            if not directory_path.is_dir():
                self.logger.error("Error: The path provided is not a valid directory\n")
                return None
            return str(directory_path)
        except Exception as e:
            self.logger.error(
                f" error the get valid directory function crashed see the error : {e}\n"
            )
            raise

    def list_files_and_folders(self, directory_path: str) -> List[str]:
        try:
            path = Path(directory_path)
            content = list(path.iterdir())

            if not content:
                self.logger.error("Error: There are no files or folders here\n")
                return []

            print(f"\nItems in folder: {directory_path}\n")
            for index, item in enumerate(content, 1):
                item_type = "📁" if item.is_dir() else "📄"
                self.logger.info(f"{index}. {item_type} {item.name}\n")
            return [str(item) for item in content]
        except Exception as e:
            self.logger.error(
                f"Error accessing directory and listing it's content: {e}\n"
            )
            raise

    def get_valid_files_indices(self, max_index: int) -> List[int]:
        if max_index == 0:
            self.logger.warning("Sorry, empty folder - nothing to index\n")
            return []

        while True:
            indices_input = input(
                "\nEnter the file numbers to process (comma-separated, e.g., 1,3): \n"
            )
            try:
                indices = [
                    int(i.strip()) - 1
                    for i in indices_input.split(",")
                    if i.strip().isdigit()
                ]
                invalid_indices = [i + 1 for i in indices if i < 0 or i >= max_index]

                if invalid_indices:
                    print(f"Invalid selection(s): {invalid_indices}. Please try again.")
                    continue

                return indices
            except ValueError:
                self.logger.error("Invalid input. Please enter valid numbers\n")
