from pathlib import Path
import datetime,csv

SCRIPT_PATH = Path( __file__ ).absolute()
LOG_FOLDER_PATH = SCRIPT_PATH.parent / "logs"

def append_to_txt_file(device = "DEFAULT_DEVICE", operation_tag = "DEFAULT_OPERATION_TAG", tag = "DEFAULT_TAG", data ="NO DATA" ,file_name_w_extension = "default.txt" ):
    global LOG_FOLDER_PATH
    text_PATH = LOG_FOLDER_PATH / file_name_w_extension  
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    text  = f"{year},{month},{day},{hour},{minute},{second},{operation_tag},{device},{tag},{data}\n"

    with open(text_PATH, 'a+') as file:
        file.write(text)


def append_to_csv_file(device = "DEFAULT_DEVICE", device_tag="DEFAULT_DEVICE_TAG",operation_tag = "DEFAULT_OPERATION_TAG", tag = "DEFAULT_TAG", data ="NO DATA" ,file_name_w_extension = "default_2.csv" ):
    # Open the CSV file in 'append' mode
    global LOG_FOLDER_PATH
    csv_PATH = LOG_FOLDER_PATH / file_name_w_extension  
    
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second

    with open(csv_PATH, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # Append a new row to the CSV file
        row = [str(year), str(month), str(day), str(hour), str(minute), str(second), str(operation_tag), str(device), str(device_tag), str(tag), str(data) ]
        writer.writerow(row)

    pass





