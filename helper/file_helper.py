import os
import sys
from PIL import Image

def get_cli_args(default_lang="eng"):
    """
    Parses command-line arguments to get:
      - directory path (default = current working directory)
      - OCR language (default = 'eng')
    Returns:
      (dir_path, lang)
    """
    dir_path = os.getcwd()
    lang = default_lang

    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    if len(sys.argv) > 2:
        lang = sys.argv[2]

    return dir_path, lang

def get_image_file_names(dir_path):
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
    return image_files