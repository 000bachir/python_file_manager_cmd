"""
this will check if a file a file is a valid pdf file by looking at the file signature
"""


def valid_pdf(filename: str) -> bool:
    try:
        with open(filename, "rb") as f:
            header = f.read(4)
            if header == b"%PDF":
                print("valid pdf file")
                return True
            else:
                print("invalid pdf file")
                return False
    except FileNotFoundError:
        print(f"error file not found : {filename}")
        return False
    except Exception as e:
        print(f"error the validation failed {e}")
        return False
