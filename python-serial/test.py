import random,time

import serial_module
import BQ225

def connet_to_master_device(MasterSerial:serial_module.MasterDevice):
    while(True):
        is_connected = MasterSerial.connect_to_first_not_blocked_port()
        if not is_connected:continue
        
        is_master_device = MasterSerial.is_master_device()
        if is_master_device:
            print("Master device found")
            break
        else:
            print("Master device not found")
            MasterSerial.disconnect(should_block=True)

def get_humidity_from_BQ225(BQ225_sensor:BQ225.BQ225, MasterSerial:serial_module.MasterDevice):
    #get humidity
    data_count, data_bytes = BQ225_sensor.form_humidity_data_package_16_bytes()    
    MasterSerial.transmit_data_package_to_lora_node(function_code=1, slave_lora_address = BQ225_sensor.lora_address, request_data_count=data_count, request_data_bytes=data_bytes)
    raw_response = MasterSerial.read_serial_until_newline(throw_exception_on_empty_line=False)
    processed_response = MasterSerial.categorize_and_format_response(raw_response)
    print(processed_response)
    if processed_response[0] ==200:
        BQ225_sensor.analyze_humidity_request_response(processed_response[1], print_humidty = True)

def get_temperature_from_BQ225(BQ225_sensor:BQ225.BQ225, MasterSerial:serial_module.MasterDevice):
        #get temperature
        data_count, data_bytes = BQ225_sensor.form_temperature_data_package_16_bytes()  
        MasterSerial.transmit_data_package_to_lora_node(function_code=1, slave_lora_address =BQ225_sensor.lora_address, request_data_count=data_count, request_data_bytes=data_bytes)
        raw_response = MasterSerial.read_serial_until_newline(throw_exception_on_empty_line=False)
        processed_response = MasterSerial.categorize_and_format_response(raw_response)
        print(processed_response)
        if processed_response[0] ==200:
            BQ225_sensor.analyze_temperature_request_response(processed_response[1], print_temperature = True)

while(True):
    #create device objects
    BQ225_sensor = BQ225.BQ225(lora_address=2, slave_ID=141)
    MasterSerial = serial_module.MasterDevice()

    #(1) Try to connect to the master device
    connet_to_master_device(MasterSerial=MasterSerial)

    #(2) Run the main loop
    while(True):         
        get_humidity_from_BQ225(BQ225_sensor=BQ225_sensor, MasterSerial=MasterSerial)
        get_temperature_from_BQ225(BQ225_sensor=BQ225_sensor, MasterSerial=MasterSerial)

      
    




