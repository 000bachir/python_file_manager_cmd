import os
import sys
import secrets
import base64
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from typing import Optional, List, Tuple

class GettingValidDirectory:
    def __init__(self) -> None:
        self.validate_response = {"encrypt", "decrypt"}

    def get_user_input(self, prompt: str, validate_options: Optional[set[str]] = None) -> str:
        while True:
            response = input(prompt).strip().lower()
            if validate_options is None or response in validate_options:
                return response
            print(f"Please enter one of the following options: {', '.join(validate_options)}")
    
    def get_valid_source_directory(self) -> Optional[str]:
        directory_path = input("Please enter the directory where the files are located: ")
        directory_path = os.path.abspath(directory_path)  # Convert to absolute path
        print(f"Checking directory: {directory_path}")
        
        if not os.path.exists(directory_path):
            print(f"Error: The directory path provided is wrong: {directory_path}")
            return None
        if not os.path.isdir(directory_path):
            print("Error: The path is not a valid directory")
            return None
        return directory_path

    def get_files_in_directory_path(self, directory_path: str) -> List[str]:
        try:
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            if not files:
                print("Error: There are no files in this directory")
                return []
            print("\nFiles in folder:")
            for index, file in enumerate(files, 1):
                print(f"{index}. {file}")
            return files
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return []
    
    def get_valid_file_indices(self, max_index: int) -> List[int]:
        while True:
            indices_input = input("\nEnter the file numbers to process (comma-separated, e.g., 1,3): ")
            try:
                indices = [
                    int(i.strip()) - 1 for i in indices_input.split(",")
                    if i.strip().isdigit()
                ]
                print(f"Selected indices: {indices}")  # Debug print
                
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

class FileEncryptor:
    def __init__(self) -> None:
        self.Get_Valid_Directory = GettingValidDirectory()
        self.Key_Manager = KeyManager()
        self.fernet = None

    def initialize_encryption(self, password: str, key_storage_path: Optional[str] = None) -> None:
        try:
            derived_key, salt = self.Key_Manager.generate_key(password)
            print(f"Initializing Fernet with key of length: {len(derived_key)} bytes")  # Debug print
            
            if key_storage_path:
                print(f"Saving key to: {key_storage_path}")  # Debug print
                self.Key_Manager.save_key_to_file(derived_key, salt, directory=key_storage_path)
                print(f"Saved key to: {key_storage_path} Successfully")  # Debug print

            self.fernet = Fernet(derived_key)
            print("Fernet initialization successful")  # Debug print
        except Exception as e:
            print(f"Error initializing encryption: {e}")
            raise  # Re-raise the exception for debugging

    def process_files(self, source_directory: str, selected_files: List[str], operation: str) -> None:
        print(f"\nProcessing files in directory: {source_directory}")  # Debug print
        print(f"Operation: {operation}")  # Debug print
        print(f"Selected files: {selected_files}")  # Debug print
        
        if not self.fernet:
            print("Error: Encryption system not initialized")
            return

        # Create output directory
        output_dir = os.path.join(os.path.dirname(source_directory), f"{os.path.basename(source_directory)}_{operation}")
        os.makedirs(output_dir, exist_ok=True)
        print(f"Creating output directory ,Files will be saved to: {output_dir}")  # Debug print

        for file_name in selected_files:
            source_path = os.path.join(source_directory, file_name)
            dest_path = os.path.join(output_dir, f"{file_name}.encrypted" if operation == "encrypt" else file_name.replace(".encrypted", ""))
            
            print(f"\nProcessing file: {file_name}")  # Debug print
            print(f"Source path: {source_path}")  # Debug print
            print(f"Destination path: {dest_path}")  # Debug print
            if operation == "encrypt":
                dest_path = os.path.join(output_dir, f"{file_name}.encrypted")
            else:  # decrypt
            # Remove .encrypted extension if present
                base_name = file_name
                if file_name.endswith(".encrypted"):
                    base_name = file_name[:-10]  # Remove .encrypted
                    dest_path = os.path.join(output_dir, base_name)
        
            print(f"\nProcessing file: {file_name}")
            try:
                with open(source_path, "rb") as file:
                    file_data = file.read()
                    print(f"Read {len(file_data)} bytes from source file")  # Debug print

                if operation == "encrypt":
                    processed_data = self.fernet.encrypt(file_data)
                    print(f"Encrypted data size: {len(processed_data)} bytes")  # Debug print
                elif operation == "decrypt":
                    processed_data = self.fernet.decrypt(file_data)
                    print(f"Decrypted data size: {len(processed_data)} bytes")  # Debug print

                with open(dest_path, "wb") as file:
                    file.write(processed_data)
                    print(f"Wrote {len(processed_data)} bytes to destination file")  # Debug print
                
                print(f"Successfully {operation}ed: {file_name}")
                
                # Verify file was created
                if os.path.exists(dest_path):
                    print(f"Verified: Output file exists at {dest_path}")
                    print(f"Output file size: {os.path.getsize(dest_path)} bytes")
                else:
                    print("Error: Output file was not created!")

            except InvalidToken:
                print(f"Error: Invalid key for file {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
                import traceback
                print(traceback.format_exc())  # Print full error traceback

class DecryptionHandler:
    def __init__(self):
        self.fernet = None
        
    def load_key_from_file(self, key_path: str) -> Tuple[bytes, bytes]:
        """
        Load the encryption key and salt from a key file.
        
        Args:
            key_path: Path to the key file
            
        Returns:
            Tuple containing (key, salt)
        """
        try:
            with open(key_path, 'rb') as key_file:
                # content = key_file.read().split(b'\n')
                content  = key_file.read()
                parts = content.split(b'||SALT|')
                if len(parts) != 2:
                    raise ValueError(f"Invalid key file format Got {len(parts)} parts instead of 2")
                return parts[0], parts[1]  # key, salt
        except Exception as e:
            print(f"Error loading key file: {e}")
            raise

    def initialize_decryption(self, key_path: str , password : Optional[str] = None) -> bool:
        """
        Initialize the decryption system using a saved key file.
        
        Args:
            key_path: Path to the key file
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            key, salt= self.load_key_from_file(key_path)
            if not password :
                self.fernet = Fernet(key)
            else : 
                # Re-derive the key using salt and password
                    key_manager = KeyManager()
                    derived_key = key_manager.derive_from_key(salt, password)
                    encoded_key = base64.urlsafe_b64encode(derived_key)
                    self.fernet = Fernet(encoded_key)
            return True
        except Exception as e:
            print(f"Failed to initialize decryption: {e}")
            return False

    def decrypt_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """
        Decrypt a single file using the loaded key.
        
        Args:
            input_path: Path to the encrypted file
            output_path: Optional path for the decrypted file. If not provided,
                        removes '.encrypted' from the input path
                        
        Returns:
            bool: True if decryption was successful
        """
        if not self.fernet:
            print("Decryption not initialized. Please load a key first.")
            return False

        try:
            # If no output path provided, create one by removing .encrypted extension
            if not output_path:
                output_path = input_path.replace('.encrypted', '')
                if output_path == input_path:
                    base, ext = os.path.splitext(input_path)
                    output_path = f"{base}_decrypted{ext}"

            # Read encrypted data
            with open(input_path, 'rb') as file:
                encrypted_data = file.read()

            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data)

            # Write decrypted data
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)

            print(f"Successfully decrypted: {os.path.basename(input_path)}")
            return True

        except InvalidToken:
            print(f"Error: Invalid key for file {input_path}")
            return False
        except Exception as e:
            print(f"Error decrypting file {input_path}: {e}")
            return False

    def decrypt_directory(self, input_dir: str, output_dir: Optional[str] = None) -> bool:
        """
        Decrypt all encrypted files in a directory.
        
        Args:
            input_dir: Directory containing encrypted files
            output_dir: Optional directory for decrypted files. If not provided,
                       creates a 'decrypted' subdirectory
                       
        Returns:
            bool: True if all files were processed successfully
        """
        if not os.path.exists(input_dir):
            print(f"Input directory does not exist: {input_dir}")
            return False

        # Set up output directory
        if not output_dir:
            output_dir = os.path.join(input_dir, 'decrypted')
        os.makedirs(output_dir, exist_ok=True)

        success = True
        # Process each file in the directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.encrypted') or filename.endswith('.enc'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename.replace('.encrypted', '').replace('.enc', ''))
                
                if not self.decrypt_file(input_path, output_path):
                    success = False

        return success

# def main():
#     try:
#         dir_manager = GettingValidDirectory()
#         encryptor = FileEncryptor()
#         decryptor = DecryptionHandler()

#         operation = dir_manager.get_user_input(
#             "Would you like to encrypt or decrypt files? (encrypt/decrypt): ",
#             dir_manager.validate_response
#         )
#         print(f"Selected operation: {operation}")  # Debug print

#         if operation == "encrypt" :
#             password = getpass("Enter your encryption password: ")
#             print(f"Received password of length: {len(password)}")  # Debug print

#             key_storage = input("Enter directory to store the encryption key (press Enter to skip saving): ").strip()
#             if key_storage:
#                 print(f"Will store key in: {key_storage}")  # Debug print

#             encryptor.initialize_encryption(password, key_storage if key_storage else None)

#             while True:
#                 source_dir = dir_manager.get_valid_source_directory()
#                 if source_dir:
#                     break
#                 print("Please try again with a valid directory.")

#             files = dir_manager.get_files_in_directory_path(source_dir)
#             if not files:
#                 print("No files to process. Exiting.")
#                 return

#             selected_indices = dir_manager.get_valid_file_indices(len(files))
#             selected_files = [files[i] for i in selected_indices]
#             print(f"Files to process: {selected_files}")  # Debug print

#             encryptor.process_files(source_dir, selected_files, operation)
#         elif operation == "decrypt" :
#              # Get path to key file
#             key_path = input("Enter the path to your key file: ").strip()
            
#             # Initialize decryption with the key
#             if not decryptor.initialize_decryption(key_path):
#                 print("Failed to initialize decryption. Exiting.")
#                 return

#             # Get input path (file or directory)
#             input_path = input("Enter the path to the encrypted file or directory: ").strip()
            
#             if os.path.isfile(input_path):
#                 # Decrypt single file
#                 decryptor.decrypt_file(input_path)
#             elif os.path.isdir(input_path):
#                 # Decrypt entire directory
#                 decryptor.decrypt_directory(input_path)
#             else:
#                 print("Invalid path provided.")
#         else :
#             print("Program Stoping")
#     except Exception as e:
#         print(f"An error occurred in main: {str(e)}")
#         import traceback
#         print(traceback.format_exc())  # Print full error traceback

# if __name__ == "__main__":
#     main()


def main():
    try:
        dir_manager = GettingValidDirectory()
        encryptor = FileEncryptor()
        
        operation = dir_manager.get_user_input(
            "Would you like to encrypt or decrypt files? (encrypt/decrypt): ",
            dir_manager.validate_response
        )
        
        if operation == "encrypt":
            # Handle encryption
            password = getpass("Enter your encryption password: ")
            if not password:
                print("Password cannot be empty. Exiting.")
                return
                
            # Get key storage information
            key_storage = input("Enter directory to store the encryption key: ").strip()
            if not key_storage:
                print("Key storage path is required. Exiting.")
                return
                
            key_filename = input("Enter key filename (default: key.key): ").strip() or "key.key"
            
            # Initialize encryption
            try:
                encryptor.initialize_encryption(password, key_storage)
            except Exception as e:
                print(f"Failed to initialize encryption: {e}")
                return
                
            # Get source directory
            while True:
                source_dir = dir_manager.get_valid_source_directory()
                if source_dir:
                    break
                retry = input("Try again with another directory? (yes/no): ").strip().lower()
                if retry != "yes":
                    print("Operation cancelled.")
                    return
            
            # Get files to process
            files = dir_manager.get_files_in_directory_path(source_dir)
            if not files:
                print("No files to process. Exiting.")
                return
                
            selected_indices = dir_manager.get_valid_file_indices(len(files))
            selected_files = [files[i] for i in selected_indices]
            
            # Process files
            encryptor.process_files(source_dir, selected_files, operation)
            
            # Save key
            encryptor.Key_Manager.save_key_to_file(key=encryptor.fernet._key, 
                                                 salt=encryptor.Key_Manager.generate_salt_for_key(), 
                                                 directory=key_storage,
                                                 filename=key_filename)
            
        elif operation == "decrypt":
            # Handle decryption
            decryptor = DecryptionHandler()
            
            # Get key file path
            key_path = input("Enter the path to your key file: ").strip()
            if not os.path.exists(key_path):
                print(f"Key file not found: {key_path}")
                return
                
            # Ask for password if needed
            use_password = dir_manager.get_user_input(
                "Do you have a password for this key? (yes/no): ",
                {"yes", "no"}
            )
            
            password = None
            if use_password == "yes":
                password = getpass("Enter your decryption password: ")
            
            # Initialize decryption
            if not decryptor.initialize_decryption(key_path, password):
                print("Failed to initialize decryption. Exiting.")
                return
            
            # Get file or directory to decrypt
            while True:
                path = input("Enter the path to the encrypted file or directory: ").strip()
                if os.path.exists(path):
                    break
                print(f"Path does not exist: {path}")
                retry = input("Try again? (yes/no): ").strip().lower()
                if retry != "yes":
                    print("Operation cancelled.")
                    return
            
            # Process decryption
            if os.path.isfile(path):
                output_path = input("Enter output path for decrypted file (or press Enter for default): ").strip()
                decryptor.decrypt_file(path, output_path)
            elif os.path.isdir(path):
                output_dir = input("Enter output directory for decrypted files (or press Enter for default): ").strip()
                decryptor.decrypt_directory(path, output_dir)
        
        print("Operation completed.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
     main()
