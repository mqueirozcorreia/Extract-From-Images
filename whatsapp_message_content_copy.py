import pyperclip
import helper.whatsapp_helper as wh

clipboard_text = pyperclip.paste()

extracted_data_list = wh.extract_message(clipboard_text)
print(extracted_data_list)

message_list = [inner_list[3] for inner_list in extracted_data_list if len(inner_list) > 2]
print(message_list)

pyperclip.copy("\n".join(message_list))