from pathlib import Path
from typing import List, Optional

folder_path = ""


def list_contents_of_selected_folder(folder_path: str) -> Optional[List[str]]:
    print(f"Contents of folder: {folder_path}\n")
    try:
        items = list(Path(folder_path))
        if not items:
            print("error, the folder is empty\n")
        else:
            for item in items:
                print(f"-{item.name}")
    except Exception as e:
        print(f"error listing the content of the folder : {e}\n")
        raise


list_contents_of_selected_folder()
