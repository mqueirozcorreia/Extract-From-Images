import re
import csv

pattern = r"(?s)\[(\d{2}:\d{2}), (\d{2}\/\d{2}\/\d{4})\] (.*?):(?P<message>.*?)(?=\n\[\d{2}:\d{2}, \d{2}\/\d{2}\/\d{4}\]|\Z)"

def extract_messages_from_file(input_file):
    # Lê o arquivo de entrada
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    return extract_message(text)

def extract_message(text: str) -> list[list[str]]:
    """
    Returns:
        list[list[str]]: List of Messages (first list), inner list as message containing time, date, sender, message.
    """            
    matches = re.finditer(pattern, text)
    
    extracted_data_array = []
    
    for match in matches:
        time = match.group(1)
        date = match.group(2)
        sender = match.group(3)
        message = match.group("message").strip()

        extracted_data_array.append([time, date, sender, message])

    return extracted_data_array