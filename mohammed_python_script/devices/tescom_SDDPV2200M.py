import random,time
import useful_methods

class Tescom_SDDPV2200M():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.__motor_state = None #5:stopped, 1:running
        self.__VFD_frequency = None #Hz
        self.__DC_voltage = None #V

        self.__driver_reference_voltage = None #V
        
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
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_driver_run_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as validdriver run response response " + str(response))
            return False

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if True or (package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4): #TODO: the condition is always true. The package is not always 7 bytes long but the last bytes are always 255. Thus ignored this check for now
                motor_state_significant_byte = package_bytes[31]
                motor_state_least_byte = package_bytes[32]
                self.__motor_state = motor_state_significant_byte*256 +motor_state_least_byte
                print(time.strftime("%H:%M:%S", time.localtime()),"Motor state: (1: run, 5: stop):".ljust(40,"-"),self.__motor_state)
                return True
            else:
                return False

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
    
    # 15,6,15,2,sig,lst
    def set_driver_reference_voltage_dict(self, reference_voltage = None):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        reference_voltage = int(round(reference_voltage))
        if (reference_voltage < 350 or reference_voltage > 410):#TODO remove false
            raise Exception("Reference voltage must be between 350 and 410 (V)")      
        
        sig_byte = int((reference_voltage*10)/256)
        lst_byte = (reference_voltage*10)& 0xFF

        request_identifier_16_bit = random.randint(0,65535)        
        modbus_command_bytes = [self.__slave_address,6,15,2,sig_byte,lst_byte]        
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
    
    def is_valid_driver_reference_voltage_response(self,response):
            #TODO: validate CRC
            if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_driver_reference_voltage_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
            response_status = response[0]
            package_bytes = response[1]

            if response_status != True:
                if(self.IS_DEBUGGING):print("This reponse is not classified as set is_valid_driver_reference_voltage_response " + str(response_status))
                return False
            

            if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
                if package_bytes[27]==self.__slave_address and package_bytes[28]==6:
                    driver_dc_reference_significant_byte= package_bytes[31]
                    driver_dc_reference_least_byte = package_bytes[32]
                    self.__driver_reference_voltage = (driver_dc_reference_significant_byte*256 +driver_dc_reference_least_byte) /10.0
                    print(time.strftime("%H:%M:%S", time.localtime()),"Driver voltage reference (V):".ljust(40,"-"),self.__driver_reference_voltage)
                    return True
               
            return False
    
  




    def get_Tescom_SDDPV2200M_DC_voltage(self):
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

    def is_valid_get_Tescom_SDDPV2200M_DC_voltage_response(self,response):
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_get_Tescom_SDDPV2200M_DC_voltage_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as valid is_valid_get_Tescom_SDDPV2200M_DC_voltage_response " + str(response))
            return False

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if (package_bytes[27]==self.__slave_address and package_bytes[28]==3): #TODO: the condition is always true. The package is not always 7 bytes long but the last bytes are always 255. Thus ignored this check for now
                DC_voltage_significant_byte = package_bytes[30]
                DC_voltage_least_byte = package_bytes[31]
                self.__DC_voltage = (DC_voltage_significant_byte*256 + DC_voltage_least_byte)/10
                print(time.strftime("%H:%M:%S", time.localtime()),"DC voltage (V):".ljust(40,"-"),self.__DC_voltage)
                return True
        
        return False

    def get_Tescom_SDDPV2200M_driver_VFD_frequency_dict(self):
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

    def is_valid_get_Tescom_SDDPV2200M_driver_VFD_frequency_response(self,response):
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_get_Tescom_SDDPV2200M_driver_VFD_frequency_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as valid is_valid_get_Tescom_SDDPV2200M_driver_VFD_frequency_response " + str(response))
            return False

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if (package_bytes[27]==self.__slave_address and package_bytes[28]==3): #TODO: the condition is always true. The package is not always 7 bytes long but the last bytes are always 255. Thus ignored this check for now
                VFD_frequency_significant_byte = package_bytes[30]
                VFD_frequency_least_byte = package_bytes[31]
                self.__VFD_frequency = (VFD_frequency_significant_byte*256 +VFD_frequency_least_byte)/100
                print(time.strftime("%H:%M:%S", time.localtime()),"VFD frequency (Hz):".ljust(40,"-"),self.__VFD_frequency)
                return True
        return False