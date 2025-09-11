import os
import secrets
import base64
# from getpass import getpass
# from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from typing import Optional, List, Tuple


class KeyManager:
    def generate_salt_for_key(self, size: int = 16) -> bytes:
        salt = secrets.token_bytes(size)
        print(f"Generated salt of size: {len(salt)} bytes")  # Debug print
        return salt
    
    def derive_from_key(self, salt: bytes, password: str) -> bytes:
        print(f"Deriving key from password of length: {len(password)}")  # Debug print
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1
        )
        key = kdf.derive(password.encode())
        print(f"Derived key of length: {len(key)} bytes")  # Debug print
        return key

    def generate_key(self, password: str, salt_size: int = 16) -> Tuple[bytes, bytes]:
        if not password:
            raise ValueError("Password cannot be empty")
        if salt_size < 16:
            raise ValueError("Salt size must be at least 16 bytes.")
        
        salt = self.generate_salt_for_key(salt_size)
        derived_key = self.derive_from_key(salt, password)
        encoded_key = base64.urlsafe_b64encode(derived_key)
        print(f"Generated base64 encoded key of length: {len(encoded_key)} bytes")  # Debug print
        return encoded_key, salt
    
    def save_key_to_file(self , key:bytes , salt : bytes , directory : str , filename : str = "key.key") ->None :
        if not os.path.exists(directory) :
            generated_directory = input(f"The directory '{directory}' does not exist. Do you want to create it? (yes / no): ").strip().lower()
            if generated_directory == "yes" :
                os.makedirs(directory)
                print(f"Directory '{directory}' created successfully.")
            else :
                print("Operation cancelled. Key not saved")
                return
        #saving key to file
        file_path = os.path.join(directory , filename)
        try :
            with open(file_path , "wb") as key_file :
                # key_file.write(b"\n".join([key , salt]))
                # Use a clear separator that won't be in base64 encoded data
                key_file.write(key + b"||SALT||" + salt)  # Changed separator
            print(f"Key saved successfully at: {file_path}")
        except Exception as E :
            print(f"An error occurred while saving the key: {E}")
