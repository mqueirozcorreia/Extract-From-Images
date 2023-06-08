from PIL import ImageGrab
import image_helper
import pyperclip


# Capture the screen region containing the image
img = ImageGrab.grabclipboard()

# Check if an image was found in the clipboard
if img is None:
    print("No image found in clipboard")
else:
    text = image_helper.extract_text_from_image("eng", "from_memory", img)
    # Set the text to the clipboard
    pyperclip.copy(text)
    print("text copied to clipboard")