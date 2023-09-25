# Install  Tesseract
```
# Option 1
sudo apt install tesseract-ocr

# Option 2, using brew
brew install tesseract
```

## Install Languages
The English language is already included in this installation. If you want to install other language packs check : https://github.com/tesseract-ocr/tessdata/tree/main

For example, check existing languages:
```
tesseract --list-langs
```

If you are missing a language, go to the tessdata directory listed from the last command, for example
```
cd /usr/local/share/tessdata/
```
If installed with homebrew on M1, this can be in a different directory:
```
/opt/homebrew/Cellar/tesseract/{version}/share/tessdata
```

Notice that `/opt/homebrew/Cellar/` is the directory where homebrew install any package

Download your needed language, like portuguese:

```
curl -L -O https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata
```

Note that the quality of the extracted text will depend on the quality of the image and the performance of the OCR engine. You may need to experiment with different settings and preprocessing techniques to get the best results.

# Install requirements

```
pip install -r requirements.txt
```

# How to execute?

## 1 From File
Execute the command below to create text files from all files in the directory. 
For path the default is current project directory, but you can use `~/Downloads`
For lang the default is `eng` but you can use others like `por`
File are save in running directory
```
python from-file.py <path> <lang>
```

## 2 From Memory
If you have images in clipboard, will extract text from that
File are save clipboard again and in the running directory as `from_memory.txt`

```
python from-memory
```