import random,time
import useful_methods

class Growatt_SPF5000ES():
    def __init__(self, lora_address = None, slave_address = None, is_debugging = False, print_BESS_voltage = False, print_load_power = False, print_pv_power = False, print_grid_power = False):
        if lora_address == None or slave_address == None :raise Exception
        if lora_address > 65535 or lora_address<0 :raise Exception
        if slave_address > 255 or slave_address<0 :raise Exception

        self.__lora_address = lora_address
        self.__slave_address = slave_address

        self.IS_DEBUGGING = is_debugging
       
        self.__BESS_voltage= None
        self.__load_power = None
        self.__pv_power = None 
        self.__grid_power = None
        self.__BESS_power = None
        self.__BESS_current = None
        self.__inverter_charging_current = None

        self.PRINT_BESS_VOLTAGE = print_BESS_voltage
        self.PRINT_LOAD_POWER = print_load_power
        self.PRINT_PV_POWER = print_pv_power
        self.PRINT_GRID_POWER = print_grid_power

    def getter_BESS_voltage(self):
        return self.__BESS_voltage
    def getter_load_power(self):
        return self.__load_power
    def getter_pv_power(self):
        return self.__pv_power
    def getter_grid_power(self):
        return self.__grid_power
    
    def calculate_BESS_power(self):
        if self. __pv_power != None and self.__grid_power != None and self.__load_power != None:
            self.__BESS_power = (self.__pv_power + self.__grid_power) - self.__load_power
            return self.__BESS_power
        else:
            raise Exception( "BESS power cannot be calculated because one of the following is None: pv_power, grid_power, load_power")
    def calculate_BESS_current(self):
        self.__BESS_current = self.__BESS_power/self.__BESS_voltage
        return self.__BESS_current
    
    def get_slave_address(self):
        return self.__slave_address
 
    def get_lora_address(self):
        return self.__lora_address
    
    def BESS_voltage_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,4,0,17,0,1]        
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

    def is_valid_BESS_voltage_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_BESS_voltage_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as BESS voltage " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0:
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4:
                BESS_voltage_significant_byte = package_bytes[30]
                BESS_voltage_least_byte = package_bytes[31]
                BESS_voltage = BESS_voltage_significant_byte*256 + BESS_voltage_least_byte
                self.__BESS_voltage = BESS_voltage/100
                if(self.PRINT_BESS_VOLTAGE):print(time.strftime("%H:%M:%S", time.localtime()),"BESS voltage (V):".ljust(40,"-"),self.__BESS_voltage)
                return True
            else:
                print("error 1")
                return False
        else:
            print("error 2")
            return False
  
    def load_power_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,4,0,10,0,1]        
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

    def is_valid_load_power_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_load_power_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as load power" + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0:
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4:
                load_power_significant_byte = package_bytes[30]
                load_power_least_byte = package_bytes[31]
                load_power = load_power_significant_byte*256 + load_power_least_byte
                self.__load_power = load_power/10
                if(self.PRINT_LOAD_POWER):print(time.strftime("%H:%M:%S", time.localtime()),"Load Power (W):".ljust(40,"-"),self.__load_power)
                return True
            else:
                return False
  
    def pv_power_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,4,0,4,0,1]        
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

    def is_valid_pv_power_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_pv_power_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as pv power response " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4:
                pv_power_significant_byte = package_bytes[30]
                pv_power_least_byte = package_bytes[31]
                pv_power = pv_power_significant_byte*256 + pv_power_least_byte
                self.__pv_power = pv_power/10
                if(self.PRINT_PV_POWER):print(time.strftime("%H:%M:%S", time.localtime()),"PV Power (W):".ljust(40,"-"),self.__pv_power)
                return True
            else:
                return False
  
    def grid_power_request_dict(self):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        request_identifier_16_bit = random.randint(0,65535)
        
        modbus_command_bytes = [self.__slave_address,4,0,37,0,1]        
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

    def is_valid_grid_power_response(self,response):
        #TODO: validate CRC
        if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_grid_power_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            if(self.IS_DEBUGGING):print("This reponse is not classified as grid power response " + str(response_status))
            return False
        

        if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
            if package_bytes[26]==7 and package_bytes[27]==self.__slave_address and package_bytes[28]==4:
                grid_power_significant_byte = package_bytes[30]
                grid_power_least_byte = package_bytes[31]
                grid_power = grid_power_significant_byte*256 +grid_power_least_byte
                self.__grid_power = grid_power/10
                if(self.PRINT_GRID_POWER):print(time.strftime("%H:%M:%S", time.localtime()),"Grid Power (W):".ljust(40,"-"),self.__grid_power)
                return True
            else:
                return False
  
    def set_inverter_charging_current_dict(self, charging_current):
        if self.__lora_address is None:raise Exception
        if self.__slave_address is None:raise Exception

        charging_current = int(round(charging_current))
        if charging_current < 0 or charging_current > 50:
            raise Exception("Charging current must be between 0 and 50 (A)")
        else:
            self.__inverter_charging_current = charging_current            
        
        sig_byte = 0
        lst_byte = charging_current

        request_identifier_16_bit = random.randint(0,65535)        
        modbus_command_bytes = [self.__slave_address,6,0,34,sig_byte,lst_byte]        
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
    
    def is_valid_set_inverter_charging_current_response(self,response):
            #TODO: validate CRC
            if(self.IS_DEBUGGING):print("\n",time.strftime("%H:%M:%S", time.localtime()),"is_valid_set_inverter_charging_current_response: " + str(response[0])+"\n"+str(response[1])+"\n"+str(response[2]))
            response_status = response[0]
            package_bytes = response[1]

            if response_status != True:
                if(self.IS_DEBUGGING):print("This reponse is not classified as set inverter charging current " + str(response_status))
                return False
            

            if package_bytes[0] == 255 and package_bytes[3] == 2 and package_bytes[4] == 0: 
                if package_bytes[26]==8 and package_bytes[27]==self.__slave_address and package_bytes[28]==6:
                    inverter_charging_current_significant_byte = package_bytes[31]
                    inverter_charging_current_least_byte = package_bytes[32]
                    self.__inverter_charging_current = inverter_charging_current_significant_byte*256 +inverter_charging_current_least_byte
                    if(self.PRINT_GRID_POWER):print(time.strftime("%H:%M:%S", time.localtime()),"Inverter charging current (A):".ljust(40,"-"),self.__inverter_charging_current)
                    return True
                else:
                    return False
    
