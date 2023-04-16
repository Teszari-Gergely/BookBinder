import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import re


def delete_non_jpg_files(folder_path):
    print('Deleting non-jpg files...')
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    processed = 0
    total = len(subfolders)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.jpg'):
                os.remove(os.path.join(root, file))
        processed += 1
        print(f"Progress: {processed} / {total}")


def rename_jpg_files(folder_path):
    print('Renaming jpg files...')
    subfolders = sum(1 for _ in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, _)))
    processed = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jpg'):
                if '_' in file:
                    new_name = file.split('_')[-1].split('.')[0] + '.jpg'
                    os.rename(os.path.join(root, file), os.path.join(root, new_name))
                elif not file[:-4].isdigit():
                    os.remove(os.path.join(root, file))
        processed += 1
        print(f"Progress: {processed}/{subfolders}")

def create_pdf(folder_path):
    print('Creating PDF files...')
    subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    subfolders.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
    total_subfolders = len(subfolders)
    for i, subfolder_name in enumerate(subfolders):
        chapter_num = re.search(r'Chapter\s+(\d[\d.]*)', subfolder_name)
        if chapter_num is not None:
            chapter_num = chapter_num.group(1)
        else:
            chapter_num = os.path.join(f"{subfolder_name}.pdf")
        chapter_num = chapter_num.replace('.', '-')
        pdf_filename = os.path.join(folder_path, f"{chapter_num}.pdf")
        subfolder_path = os.path.join(folder_path, subfolder_name)
        image_filenames = [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if f.endswith('.jpg')]
        if not image_filenames:
            continue
        image_filenames.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
        with open(pdf_filename, 'wb') as pdf:
            pil_images = [Image.open(filename).convert('RGB') for filename in image_filenames]
            width, height = pil_images[0].size
            total_height = sum(image.size[1] for image in pil_images)
            pdf_canvas = Image.new('RGB', (width, total_height), (255, 255, 255))
            y_offset = 0
            for image in pil_images:
                pdf_canvas.paste(image, (0, y_offset))
                y_offset += image.size[1]
            pdf_canvas.save(pdf, format='PDF')
        print(f"Progress: {i+1}/{total_subfolders}")


def main():
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory()
    delete_non_jpg_files(folder_path)
    rename_jpg_files(folder_path)
    create_pdf(folder_path)
    print('Done!')


if __name__ == '__main__':
    main()
