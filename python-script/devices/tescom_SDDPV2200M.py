import random,time
import useful_methods

class Tescom_SDDPV2200M():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False, print_humidity = False, print_temperature = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.IS_DEBUGGING = is_debugging


    def get_slave_address(self):
        return self.__slave_address
 
    def get_lora_address(self):
        return self.__lora_address
    
    def driver_run_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)

        modbus_command_bytes = [self.__slave_address,6,32,0,0,1]        
        crc, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(modbus_command_bytes)
        modbus_command_bytes.extend([crc_lst, crc_sig])

        command_dict = {
            "function_code":2,
            "sub_function_code":0,
            "slave_lora_address":self.__lora_address,
            "request_data_count":8,
            "request_data_bytes":modbus_command_bytes
            }


        return {
            "request_identifier_16":request_identifier_16_bit,
            "command_dict":command_dict
        }

    def is_valid_driver_run_response(self,response):
        print(response)

    def driver_stop_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)

        modbus_command_bytes = [self.__slave_address,6,32,0,0,5]        
        crc, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(modbus_command_bytes)
        modbus_command_bytes.extend([crc_lst, crc_sig])

        command_dict = {
            "function_code":2,
            "sub_function_code":0,
            "slave_lora_address":self.__lora_address,
            "request_data_count":8,
            "request_data_bytes":modbus_command_bytes
            }


        return {
            "request_identifier_16":request_identifier_16_bit,
            "command_dict":command_dict
        }

    def is_valid_driver_stop_response(self,response):
        print(response)

