import pytesseract
import os
from PIL import Image
import sys

# get the current directory path
dir_path = os.getcwd()
if len(sys.argv) > 1:
    dir_path = sys.argv[1]

# setting extract language
lang = 'eng'
if len(sys.argv) > 2:
    lang = sys.argv[2]


# get a list of all files in the directory
files = os.listdir(dir_path)

# loop through the list of files and filter out non-image files
image_files = []
for file in files:
    file_path = os.path.join(dir_path, file)
    try:
        with Image.open(file_path) as img:
            if img.format is not None:
                image_files.append(file)
    except IOError:
        # The file is not an image
        print("Ignoring File:" + file)

# loop through the list of files and print each filename
for image_file in image_files:
    file_path = os.path.join(dir_path, image_file)
    print(file_path + " was found and we are generating .txt from it")
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img, lang=lang)
    # open a file for writing
    with open(image_file + ".txt", "w") as file:
        # write the text to the file
        file.write(text)
