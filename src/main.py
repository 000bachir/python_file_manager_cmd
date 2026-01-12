import os
from pathlib import Path
from typing import List, Optional


source = r"~/Desktop/programming"
distination = r"~/Desktop/programming/python"


os.symlink(source, distination, target_is_directory=True)

print("link is created")
