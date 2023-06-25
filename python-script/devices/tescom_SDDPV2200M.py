import random,time
import useful_methods

class Tescom_SDDPV2200M():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False, print_humidity = False, print_temperature = False, print_dc_link_voltage = False, print_ac_frequency = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.IS_DEBUGGING = is_debugging

        self.__dc_link_voltage = None
        self.ac_frequency = None
        self.PRINT_DC_LINK_VOLTAGE = print_dc_link_voltage
        self.PRINT_AC_FREQUENCY = print_ac_frequency

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


    def driver_DC_link_voltage_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,3,18,1,0,1]        
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

    def is_valid_DC_link_voltage_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_DC_link_voltage_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as valid DC link voltage response " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==3:
                dc_link_voltage_significant_byte = package_bytes[30]
                dc_link_voltage_least_byte  = package_bytes[31]
                dc_link_voltage = dc_link_voltage_significant_byte*256 +dc_link_voltage_least_byte
                self.__dc_link_voltage = dc_link_voltage/10
                if(self.PRINT_DC_LINK_VOLTAGE):print(time.strftime("%H:%M:%S", time.localtime()),"DC link voltage(V):".ljust(40,"-"),self.__dc_link_voltage)
                return True
            else:
                return False
  

    
    
    def driver_motor_frequency_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,3,17,1,0,1]        
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

    def is_valid_driver_motor_frequency_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_driver_motor_frequency_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as valid is_valid_driver_motor_frequency_response response " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==3:
                dc_link_voltage_significant_byte = package_bytes[30]
                dc_link_voltage_least_byte  = package_bytes[31]
                dc_link_voltage = dc_link_voltage_significant_byte*256 +dc_link_voltage_least_byte
                self.__dc_link_voltage = dc_link_voltage/10
                if(self.PRINT_DC_LINK_VOLTAGE):print(time.strftime("%H:%M:%S", time.localtime()),"Electrical frequency(Hz):".ljust(40,"-"),self.__dc_link_voltage)
                return True
            else:
                return False
  

    
