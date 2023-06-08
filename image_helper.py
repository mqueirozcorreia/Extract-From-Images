import pytesseract

# loop through the list of files and print each filename
def extract_text_from_image(lang, image_file, img):
    text = pytesseract.image_to_string(img, lang=lang)
    # open a file for writing
    with open(image_file + ".txt", "w") as file:
        # write the text to the file
        file.write(text)

    return text