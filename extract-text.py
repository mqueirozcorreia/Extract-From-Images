import pytesseract
import os
from PIL import Image
import sys

# setting extract language
if len(sys.argv) > 1:
    lang = sys.argv[1]
else:
    lang = 'eng'

# get the current directory path
dir_path = os.getcwd()

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
    print(image_file + " was found and we are generating .txt from it")
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img, lang=lang)
    # open a file for writing
    with open(image_file + ".txt", "w") as file:
        # write the text to the file
        file.write(text)
