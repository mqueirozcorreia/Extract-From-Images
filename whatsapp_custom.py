import re
import helper.whatsapp_helper as wh

message_pattern = r"^(.*?)(\d{1,2}h\d{2})([\s\S]+)$"
columns = ['Hour', 'Date', 'Person', 'Message']

input_file = 'mensagens.txt'  # Arquivo de texto de entrada
output_file = 'mensagens.csv' # Nome do CSV de saída

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

extracted_data_array = wh.extract_messages_from_file(input_file)
custom_extract_from_message(extracted_data_array)
wh.save(output_file, columns, extracted_data_array)
print(f"Dados extraídos e salvos em '{output_file}' com sucesso.")
