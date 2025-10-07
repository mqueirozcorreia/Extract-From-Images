import os
from PIL import Image
import helper.file_helper as fh
import helper.image_helper as ih

dir_path, lang = fh.get_cli_args()

image_files = fh.get_image_file_names(dir_path)

for image_file in image_files:
    file_path = os.path.join(dir_path, image_file)
    print(file_path + " was found and we are generating .txt from it")
    img = Image.open(file_path)
    ih.extract_text_from_image(lang, image_file, img)