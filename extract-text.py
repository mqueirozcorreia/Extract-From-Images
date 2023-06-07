import os
from PIL import Image
import sys
import file_helper
import image_helper

# get the current directory path
dir_path = os.getcwd()
if len(sys.argv) > 1:
    dir_path = sys.argv[1]

# setting extract language
lang = 'eng'
if len(sys.argv) > 2:
    lang = sys.argv[2]

image_files = file_helper.get_image_file_names(dir_path)

for image_file in image_files:
    file_path = os.path.join(dir_path, image_file)
    print(file_path + " was found and we are generating .txt from it")
    img = Image.open(file_path)
    image_helper.extract_text_from_image(lang, image_file, img)