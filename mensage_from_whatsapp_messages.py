import re
import csv

pattern = r"(?s)\[(\d{2}:\d{2}), (\d{2}\/\d{2}\/\d{4})\] (.*?):(?P<message>.*?)(?=\n\[\d{2}:\d{2}, \d{2}\/\d{2}\/\d{4}\]|\Z)"
message_pattern = r"^(.*?)(\d{1,2}h\d{2})([\s\S]+)$"
columns = ['Hour', 'Date', 'Person', 'Message']

input_file = 'mensagens.txt'  # Arquivo de texto de entrada
output_file = 'mensagens.csv' # Nome do CSV de saída


def extract_messages(input_file):
    # Lê o arquivo de entrada
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Aplica o regex para extrair os grupos
    matches = re.finditer(pattern, text)
    
    extracted_data_array = []
    
    for match in matches:
        time = match.group(1)       # Hora
        date = match.group(2)       # Data
        sender = match.group(3)     # Remetente
        message = match.group("message").strip()  # Mensagem

        extracted_data_array.append([time, date, sender, message])

    return extracted_data_array

def custom_extract_from_message(extracted_data_array):
    for extracted_data_line in extracted_data_array:
        message = extracted_data_line[3]
        message_matches = list(re.finditer(message_pattern, message))

        if message_matches:
            tipo = message_matches[0].group(1)  # Access the first match
            hora = message_matches[0].group(2)
            resto = message_matches[0].group(3)

            resto = "\n".join([line for line in resto.splitlines() if line.strip()])  # Remove empty lines

        extracted_data_line.extend([tipo, hora, resto])

def save(output_file, columns, extracted_data):
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Cabeçalhos do CSV
        writer.writerow(columns)
        # Dados extraídos
        writer.writerows(extracted_data)

extracted_data_array = extract_messages(input_file)
custom_extract_from_message(extracted_data_array)
save(output_file, columns, extracted_data_array)
print(f"Dados extraídos e salvos em '{output_file}' com sucesso.")
