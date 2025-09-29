import os
import shutil


downloads_folder = r"C:\Users\viver\Downloads"


folders = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".avi", ".mov"],
    "Music": [".mp3", ".wav"],
    "Software": [".exe", ".msi", ".zip", ".rar"]
}


for folder in folders:
    folder_path = os.path.join(downloads_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


for filename in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, filename)


    if os.path.isfile(file_path):
        file_ext = os.path.splitext(filename)[1].lower()
        moved = False
        for folder, extensions in folders.items():
            if file_ext in extensions:
                shutil.move(file_path, os.path.join(downloads_folder, folder, filename))
                print(f"Movido: {filename} → {folder}")
                moved = True
                break
        if not moved:
            print(f"Archivo sin categoría: {filename}")
