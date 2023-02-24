import random
import useful_methods

class MasterLora():
    def __init__(self, is_debugging = False):
        self.IS_DEBUGGING = is_debugging

    def greet_request_str(self):
        package_bytes = [0]*45

        package_bytes[0]=255 #package status
        process_identifier_16_bit = random.randint(0,65535)
        package_bytes[1]= process_identifier_16_bit >> 8 #process identifier significant byte
        package_bytes[2]= process_identifier_16_bit & 0xFF #process identifier least byte
        package_bytes[3]= 1 #function code
        package_bytes[4]= 99 #sub function code
        crc_16, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(package_bytes[0:43])
        package_bytes[43] = crc_lst #crc least byte
        package_bytes[44] = crc_sig #crc significant byte

        if(self.IS_DEBUGGING):print("MasterLora.greet_message() - package_bytes: " + str(package_bytes))
        return [process_identifier_16_bit, useful_methods.convert_byte_list_to_string(package_bytes)]
    
    def is_valid_greeting_response(self,response):
        response_status = response[0]
        package_bytes = response[1]

        if response_status != True:
            return False
        
        if package_bytes[0] == 1 and package_bytes[3] == 1 and package_bytes[4] == 99:
            return True
        else:
            return False

 