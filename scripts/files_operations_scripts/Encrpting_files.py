import os
import secrets
import base64
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from typing import Optional, List, Tuple

from utils import Getting_valid_directory , Key_Manager


class FileEncryptor:
    def __init__(self) -> None:
        self.Get_Valid_Directory = Getting_valid_directory()
        self.Key_Manager = Key_Manager()
        self.fernet = None

    def initialize_encryption(self, password: str, key_storage_path: Optional[str] = None) -> None:
        try:
            self.derived_key, self.salt = self.Key_Manager.generate_key(password)
            print(f"Initializing Fernet with key of length: {len(self.derived_key)} bytes")  # Debug print
            
            if key_storage_path:
                print(f"Saving key to: {key_storage_path}")  # Debug print
                self.Key_Manager.save_key_to_file(self.derived_key, self.salt, directory=key_storage_path)
                print(f"Saved key to: {key_storage_path} Successfully")  # Debug print

            self.fernet = Fernet(self.derived_key)
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

        # Create output directory - FIXED NAMING ISSUE
        output_dir = os.path.join(os.path.dirname(source_directory), f"{operation}ed_files")
        os.makedirs(output_dir, exist_ok=True)
        print(f"Creating output directory, Files will be saved to: {output_dir}")  # Debug print

        for file_name in selected_files:
            source_path = os.path.join(source_directory, file_name)
            
            # FIXED NAMING LOGIC
            if operation == "encrypt":
                dest_path = os.path.join(output_dir, f"{file_name}.encrypted")
            else:  # decrypt
                # Remove .encrypted extension if present
                if file_name.endswith(".encrypted"):
                    base_name = file_name[:-10]  # Remove .encrypted
                else:
                    base_name = file_name
                dest_path = os.path.join(output_dir, base_name)
            
            print(f"\nProcessing file: {file_name}")
            print(f"Source path: {source_path}")  # Debug print
            print(f"Destination path: {dest_path}")  # Debug print
            
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
            # Make sure key_path is a file, not a directory
            if os.path.isdir(key_path):
                raise ValueError(f"Path is a directory, not a file: {key_path}")
                
            with open(key_path, 'rb') as key_file:
                content = key_file.read()
                # FIX: Wrong separator in the split operation
                parts = content.split(b'||SALT||')
                if len(parts) != 2:
                    raise ValueError(f"Invalid key file format: Got {len(parts)} parts instead of 2")
                return parts[0], parts[1]  # key, salt
        except Exception as e:
            print(f"Error loading key file: {e}")
            raise

    def initialize_decryption(self, key_path: str, password: Optional[str] = None) -> bool:
        """
        Initialize the decryption system using a saved key file.
        
        Args:
            key_path: Path to the key file
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            key, salt = self.load_key_from_file(key_path)
            if not password:
                self.fernet = Fernet(key)
            else: 
                # Re-derive the key using salt and password
                key_manager = Key_Manager()
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

            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

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
            output_dir = os.path.join(os.path.dirname(input_dir), 'decrypted_files')
        os.makedirs(output_dir, exist_ok=True)

        success = True
        # Process each file in the directory
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)
            
            # Skip directories
            if not os.path.isfile(input_path):
                continue
                
            if filename.endswith('.encrypted') or filename.endswith('.enc'):
                output_path = os.path.join(output_dir, filename.replace('.encrypted', '').replace('.enc', ''))
                
                if not self.decrypt_file(input_path, output_path):
                    success = False

        return success

def main():
    try:
        dir_manager = Getting_valid_directory()
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
                
            key_filename = input("Enter key filename (default: key.key): ").strip()
            if not key_filename:
                key_filename = "key.key"
            
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
            if hasattr(encryptor, 'derived_key') and hasattr(encryptor, 'salt'):
                encryptor.Key_Manager.save_key_to_file(
                    key=encryptor.derived_key,
                    salt=encryptor.salt,
                    directory=key_storage,
                    filename=key_filename
                )
            else:
                print("Error: Encryption keys not properly initialized")

            
        elif operation == "decrypt":
            # Handle decryption
            decryptor = DecryptionHandler()
            
            # Get key file path - FIXED KEY FILE PATH LOGIC
            while True:
                key_path = input("Enter the full path to your key file (including filename): ").strip()
                if os.path.isfile(key_path):
                    break
                print(f"File not found: {key_path}")
                if os.path.isdir(key_path):
                    print(f"The path you entered is a directory, not a file. Please include the filename.")
                retry = input("Try again? (yes/no): ").strip().lower()
                if retry != "yes":
                    print("Operation cancelled.")
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
                decryptor.decrypt_file(path, output_path if output_path else None)
            elif os.path.isdir(path):
                output_dir = input("Enter output directory for decrypted files (or press Enter for default): ").strip()
                decryptor.decrypt_directory(path, output_dir if output_dir else None)
        
        print("Operation completed.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()