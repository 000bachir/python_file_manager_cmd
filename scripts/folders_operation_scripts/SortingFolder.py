"""
? this is not the intended scripts i wanted to create a script that rearrange folders and files based on a alphabatical order
"""
import os
import shutil

# Specify the directory to scan
# directory = 'C:/Users/ADMIN/Desktop/sorting_folders'

# Create a dictionary of folder names and file extensions
file_types = {
    'Text_Files': ['.txt'],
    'CSV_Files': ['.csv'],
    'JSON_Files': ['.json'],
    'Excel_Files': ['.xlsx', '.xls'],
    'PDF_Files': ['.pdf'],
    'Word_Documents': ['.docx', '.doc'],
    'Image_Files': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    'Audio_Files':["mp3""wav","flac""aac","ogg","wma","alac""aiff""pcm","m4a","opus""amr","ra", "dsd","dts","mid","voc","ac3","au"],
    'Video_Files': [".avi" , ".mkv" , ".fly" , ".wmv" , ".mov",".mp4" , ".webm" , ".vob" , ".mng" , ".qt" , ".mpg", ".mpeg" , ".3gp"],
    'XML_Files': ['.xml'],
    'HTML_Files': ['.html'],
    'Archive_Files': ['.zip', '.tar', '.gz'],
    'YAML_Files': ['.yaml', '.yml']
}

# Function to organize files
def organize_files(directory):
    # Get the list of all files in the directory
    for file_name in os.listdir(directory):
        # Get the full path of the file
        file_path = os.path.join(directory, file_name)

        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue

        # Get the file extension
        _, file_extension = os.path.splitext(file_name)

        # Check the file extension and move the file to the appropriate folder
        try :
            for folder, extensions in file_types.items():
                if file_extension.lower() in extensions:
                    folder_path = os.path.join(directory, folder)
                    
                    # Create folder if it doesn't exist
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    
                    # Move the file to the corresponding folder
                    shutil.move(file_path, os.path.join(folder_path, file_name))
                    break
        except FileNotFoundError :
            print(f"Error: Directory '{directory}' not found.")
        except PermissionError : 
                    print(f"Error: Permission denied to move '{directory}'.")



def get_user_prompt(prompt) :
    return input(prompt)

def main() :
    print("Welcome to the Sorting Section Utility!!!")
    action = get_user_prompt("Would you like to move your files to a new folder? (move/quit): ").strip().lower()
    while True : 
        if action == "quit" :
            print("Thank you for using the Folder Sorting Utility. Goodbye!")
            break
        directory = input("Please enter the path where the folder(s) are located: ").strip().lower()

        if action == "move" :
            organize_files(directory)
            print("Files have been organized into respective folders.")
        else : 
            continue

if __name__ == '__main__' :
    main()


