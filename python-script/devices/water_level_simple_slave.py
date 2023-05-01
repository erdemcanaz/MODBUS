import random,time
import useful_methods

class water_level_simple_slave():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False, print_water_level = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.IS_DEBUGGING = is_debugging
        self.PRINT_WATER_LEVEL = print_water_level

        self.__water_level = None

    def getter_water_level(self):
        return self.__water_level
    
    def get_slave_address(self):
        return self.__slave_address
 
    def get_lora_address(self):
        return self.__lora_address
    
    def water_level_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)

        modbus_command_bytes = [self.__slave_address,4,0,0,0,1]        
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

    def is_valid_water_level_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_water_level_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as water level " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0:
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4:
                water_level_significant_byte = package_bytes[30]
                water_level_least_byte = package_bytes[31]
                water_level = water_level_significant_byte*256 + water_level_least_byte
                self.__water_level = water_level
                if(self.PRINT_WATER_LEVEL):print(time.strftime("%H:%M:%S", time.localtime()),"Water level (cm):".ljust(40,"-"),self.__water_level)
                return True
            else:
                return False
        
  