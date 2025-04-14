import os 
import shutil 


def testing(download_folder) : 
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.svg'],
        'Documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
        'Archives': ['.zip', '.rar', '.tar.gz']
    }
    for files in os.listdir(download_folder) :
        if os.path.isfile(os.path.join(download_folder , files)) :
            file_ext = os.path.splitext(files)[1].lower()
            destination_folder = next((ftype for ftype , exts in file_types.items() if file_ext in exts ) , 'Others')
            