import logging
import os
import secrets
import base64

# from getpass import getpass
# from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from typing import Optional, List, Tuple


class KeyManager:
    def __init__(self, enable_loggin: bool = True) -> None:
        if enable_loggin:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)
            self.logger.info("key manager class is good to go \n")

    def generate_salt_for_key(self, size: int = 16) -> bytes:
        salt = secrets.token_bytes(size)
        self.logger.info(f"Generated salt of size: {len(salt)} bytes\n")
        return salt

    def derive_from_key(self, salt: bytes, password: str) -> bytes:
        self.logger.info(f"Deriving key from password of length: {len(password)}\n")
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        key = kdf.derive(password.encode())
        self.logger.info(f"Derived key of length: {len(key)} bytes")
        return key

    def generate_key(self, password: str, salt_size: int = 16) -> Tuple[bytes, bytes]:
        if not password:
            raise ValueError("Password cannot be empty\n")
        if salt_size < 16:
            raise ValueError("Salt size must be at least 16 bytes\n")

        salt = self.generate_salt_for_key(salt_size)
        derived_key = self.derive_from_key(salt, password)
        encoded_key = base64.urlsafe_b64encode(derived_key)
        self.logger.info(
            f"Generated base64 encoded key of length: {len(encoded_key)} bytes\n"
        )
        return encoded_key, salt

    def save_key_to_file(
        self, key: bytes, salt: bytes, directory: str, filename: str = "secret_key.key"
    ) -> None:
        if not os.path.exists(directory):
            generated_directory = (
                input(
                    f"The directory '{directory}' does not exist. Do you want to create it? (yes / no): \n"
                )
                .strip()
                .lower()
            )
            if generated_directory == "yes":
                os.makedirs(directory)
                self.logger.info(f"Directory '{directory}' created successfully\n")
            else:
                self.logger.warning("Operation cancelled. Key not saved\n")
                return
        # saving key to file
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, "wb") as key_file:
                # key_file.write(b"\n".join([key , salt]))
                # need a clear separator that won't be in base64 encoded data
                key_file.write(key + b"||SALT||" + salt)  # Changed separator
            self.logger.info(f"Key saved successfully at: {file_path}\n")
        except Exception as e:
            self.logger.error(f"An error occurred while saving the key: {e}")
            raise
