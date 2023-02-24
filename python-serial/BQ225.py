import SpecificExceptions

class BQ225():
    def __init__(self, lora_address=None, slave_ID=None):
        if lora_address == None or slave_ID == None :raise SpecificExceptions.AddressIsNoneException
        if lora_address > 65535 or lora_address<0 :raise SpecificExceptions.AddressOutOfRangeException
        if slave_ID > 255 or slave_ID<0 :raise SpecificExceptions.AddressOutOfRangeException

        self.lora_address = lora_address
        self.slave_ID = slave_ID

        self.humidity_percentage = None
        self.temperature_celcius = None

    def get_slave_ID(self):
        return self.slave_ID
    def get_lora_address(self):
        return self.lora_address

    def form_humidity_data_package_16_bytes(self):
        if self.lora_address is None:raise SpecificExceptions.AddressIsNoneException
        if self.slave_ID is None:raise SpecificExceptions.AddressIsNoneException

        REQUEST_DATA_COUNT = 8
        request_data_bytes = [self.slave_ID,3,0,0,0,1]
        crc_info_list = BQ225.calculate_crc(request_data_bytes)
        request_data_bytes.append(crc_info_list[1])
        request_data_bytes.append(crc_info_list[2])
        request_data_bytes.extend([0]*(16-REQUEST_DATA_COUNT))

        return [REQUEST_DATA_COUNT, request_data_bytes]
    
    def analyze_humidity_request_response(self, response_bytes_int=None ,print_humidty = False):        
        if response_bytes_int[25]==7 and response_bytes_int[26]==self.slave_ID and  response_bytes_int[27]==3:
            humidity_significant_byte = int(response_bytes_int[29])
            humidity_least_byte = int(response_bytes_int[30])
            humidity = humidity_significant_byte*256 + humidity_least_byte
            self.humidity_percentage = humidity/100
            if(print_humidty): print("Humidity:",self.humidity_percentage)
           
        else:
            print("Humidity request failed",response_bytes_int[25],response_bytes_int[26:42])

       
    def form_temperature_data_package_16_bytes(self):
        if self.lora_address is None:raise SpecificExceptions.AddressIsNoneException
        if self.slave_ID is None:raise SpecificExceptions.AddressIsNoneException

        REQUEST_DATA_COUNT = 8
        request_data_bytes = [self.slave_ID,3,0,1,0,1]
        crc_info_list = BQ225.calculate_crc(request_data_bytes)
        request_data_bytes.append(crc_info_list[1])
        request_data_bytes.append(crc_info_list[2])
        request_data_bytes.extend([0]*(16-REQUEST_DATA_COUNT))

        return [REQUEST_DATA_COUNT, request_data_bytes]
    
    def analyze_temperature_request_response(self, response_bytes_int=None,print_temperature=False):
        
        if response_bytes_int[25]==7 and response_bytes_int[26]==self.slave_ID and  response_bytes_int[27]==3:
            temperature_significant_byte = int(response_bytes_int[29])
            temperature_least_byte = int(response_bytes_int[30])
            temperature= temperature_significant_byte*256 + temperature_least_byte
            self.temperature_celcius = temperature/100
            if(print_temperature):print("Temperature:",self.temperature_celcius)
        else:
            print("Temperature request failed",response_bytes_int[25],response_bytes_int[26:42])
         

       
    @classmethod
    def calculate_crc(cls, byte_list):
        key = 40961 # 1010 0000 0000 0001    
        result_crc = None
        initial_crc = 65535 #0xFFFF
        for i in range(len(byte_list)):
            result_crc = byte_list[i] ^ initial_crc if result_crc is None else byte_list[i] ^ result_crc

            for j in range(0,8):
                should_XOR_with_key = True if result_crc % 2 == 1 else False
                result_crc = result_crc >> 1

                if should_XOR_with_key:
                    result_crc = result_crc ^ key
        

        crc_significant_byte = result_crc >> 8
        crc_least_byte = result_crc & 0xFF
        return [result_crc,crc_least_byte, crc_significant_byte]
    