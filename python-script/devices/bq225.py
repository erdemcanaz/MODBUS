import random,time
import useful_methods

class BQ225():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False, print_humidity = False, print_temperature = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.IS_DEBUGGING = is_debugging
        self.PRINT_HUMIDITY = print_humidity
        self.PRINT_TEMPERATURE = print_temperature

        self.__humidity_percentage = None
        self.__temperature_celcius = None

    def get_slave_address(self):
        return self.__slave_address
 
    def get_lora_address(self):
        return self.__lora_address
    
    def humidity_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)

        modbus_command_bytes = [self.__slave_address,3,0,0,0,1]        
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

    def is_valid_humidity_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_humidity_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as humidity " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0:
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==3:
                humidity_significant_byte = package_bytes[30]
                humidity_least_byte = package_bytes[31]
                humidity = humidity_significant_byte*256 + humidity_least_byte
                self.__humidity_percentage = humidity/100
                if(self.PRINT_HUMIDITY):print(time.strftime("%H:%M:%S", time.localtime()),"Humidity (%):".ljust(40,"-"),self.__humidity_percentage)
                return True
            else:
                return False
        
    def temperature_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)

        modbus_command_bytes = [self.__slave_address,3,0,1,0,1]
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
    
    def is_valid_temperature_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_temperature_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as temperature " + str(response_status))
            return False
        
        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0:
            #TODO: remove 
            print(package_bytes[26],package_bytes[27],package_bytes[28],package_bytes[29],package_bytes[30],package_bytes[31],package_bytes[32])
            if True or package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==3:
                temperature_significant_byte = package_bytes[30]
                temperature_least_byte = package_bytes[31]
                temperature = temperature_significant_byte*256 + temperature_least_byte
                self.__temperature_celcius = temperature/100
                if(self.PRINT_TEMPERATURE):print(time.strftime("%H:%M:%S", time.localtime()),"Temperature (C):".ljust(40,"-"),self.__temperature_celcius)
                return True
            else:
                return False
