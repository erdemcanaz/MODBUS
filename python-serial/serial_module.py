import time,traceback,random
import serial
import serial.tools.list_ports

class MasterDevice():    
    BOOT_TIME_SECONDS = 5
    
    def __init__(self, time_out = 5, baud_rate = 9600):
        self.serial_instance = None
        self.master_address = None
        self.time_out = time_out
        self.baund_rate = baud_rate
        self.blocked_ports_list_str = []
        self.REQUEST_DATA_PACKAGE = [0]*44

    def read_serial_until_newline(self,throw_exception_on_empty_line=False):
        new_line = self.serial_instance.readline().decode("utf-8")
        if new_line == "" and throw_exception_on_empty_line:
            raise Exception("Empty line received")

        return new_line

    def get_available_bytes(self):
        return self.serial_instance.in_waiting

    def write_string_to_serial(self, string_to_write):
        self.serial_instance.write(string_to_write.encode())
    
    def connect_to_first_not_blocked_port(self):
        port_instances = list(serial.tools.list_ports.comports())

        available_ports_list_str = []
        for port_instance in port_instances:
            if port_instance.device not in self.blocked_ports_list_str:
                available_ports_list_str.append(port_instance.device)

        for available_port in available_ports_list_str:
            try:
                self.serial_instance = serial.Serial(available_port, baudrate=self.baund_rate, timeout=self.time_out)
                print("Connected to device on port: " + available_port)
                time.sleep(self.BOOT_TIME_SECONDS)
                return True

            except serial.SerialException:
                #TODO: add to blocked ports
                print("Could not connect to device on port: " + available_port)
                print("Blocking port: " + str(available_port))
                self.blocked_ports_list_str.append(available_port)
                print("Blocked ports: " + str(self.blocked_ports_list_str))
                continue
        return False

    def disconnect(self, should_block=False):
        if self.serial_instance is None:
            print("No serial instance to disconnect from")
            return

        if should_block:
            print("Blocking port: " + str(self.serial_instance.port))
            self.blocked_ports_list_str.append(self.serial_instance.port)
            print("Blocked ports: " + str(self.blocked_ports_list_str))

        print("Disconnected from: " + str(self.serial_instance.port))
        self.serial_instance.close()
        self.serial_instance = None

#_______________________________________________________________


    def overwrite_request_CRC(self):
        key = 40961 # 1010 0000 0000 0001    
        result_crc = None
        initial_crc = 65535 #0xFFFF
        for i in range(0,42):
            result_crc = self.REQUEST_DATA_PACKAGE[i] ^ initial_crc if result_crc is None else self.REQUEST_DATA_PACKAGE[i] ^ result_crc

            for j in range(0,8):
                should_XOR_with_key = True if result_crc % 2 == 1 else False
                result_crc = result_crc >> 1

                if should_XOR_with_key:
                    result_crc = result_crc ^ key
        self.REQUEST_DATA_PACKAGE[43] = result_crc >> 8
        self.REQUEST_DATA_PACKAGE[42] = result_crc & 0xFF
        return [result_crc,self.REQUEST_DATA_PACKAGE[42],self.REQUEST_DATA_PACKAGE[43]]

    def overwrite_request_process_identifier(self):
        process_identifier_16_bit = random.randint(0,65535)
        self.REQUEST_DATA_PACKAGE[0]= process_identifier_16_bit >> 8
        self.REQUEST_DATA_PACKAGE[1]= process_identifier_16_bit & 0xFF
        return [process_identifier_16_bit,self.REQUEST_DATA_PACKAGE[0],self.REQUEST_DATA_PACKAGE[1]]

    def is_master_device(self):
        EXPECTED_MASTER_RESPONSE = "Hi, As a master device, I am here to redirect your package. My address is"
        
        self.REQUEST_DATA_PACKAGE=[0]*44
        self.REQUEST_DATA_PACKAGE[2] = 99
        self.overwrite_request_process_identifier()
        self.overwrite_request_CRC()
        
        serial_str = ""
        for i in range(0,43):
            serial_str += str(self.REQUEST_DATA_PACKAGE[i]) + ","
        serial_str += str(self.REQUEST_DATA_PACKAGE[43])+ "\n"        
        self.write_string_to_serial(serial_str)

        response = self.read_serial_until_newline(throw_exception_on_empty_line = True)
        splitted_response = response.split(":")

        if splitted_response[0]==EXPECTED_MASTER_RESPONSE:
            return True
        else:
            return False

    def transmit_data_package_to_lora_node(self, function_code= None, sub_function_code = 0, slave_lora_address = None, request_data_count = 0, request_data_bytes=[]):

        if function_code is None:
            raise Exception("Function code is not defined")
        if len(request_data_bytes) != 16:
            raise Exception("Request data bytes must be 16 bytes long")

        self.REQUEST_DATA_PACKAGE=[0]*44
        self.overwrite_request_process_identifier()
        self.REQUEST_DATA_PACKAGE[2] = function_code
        self.REQUEST_DATA_PACKAGE[3] = sub_function_code
        self.REQUEST_DATA_PACKAGE[4] = 0
        self.REQUEST_DATA_PACKAGE[5] = 0
        self.REQUEST_DATA_PACKAGE[6] = slave_lora_address>>8
        self.REQUEST_DATA_PACKAGE[7] = slave_lora_address & 0xFF
        self.REQUEST_DATA_PACKAGE[8] = request_data_count
        for i in range(0,16):
            self.REQUEST_DATA_PACKAGE[9+i] = request_data_bytes[i]
        self.overwrite_request_CRC()

        text = ""
        for i in range(0,43):
            text += str(self.REQUEST_DATA_PACKAGE[i]) + ","
        text += str(self.REQUEST_DATA_PACKAGE[43])+ "\n"
        self.write_string_to_serial(text)
        return list(self.REQUEST_DATA_PACKAGE)

    def categorize_and_format_response(self, response):

        if response == "":
            return [399, None]
        elif "STATUS-400" in response:
            return [400, None]
        elif "STATUS-401" in response:
            return [401, None]
        elif "STATUS-402" in response:
            return [402, None]        
        else:            
            response_bytes_str = response.split(",")
            response_bytes = []
            for byte_str in response_bytes_str:
                response_bytes.append(int(byte_str))
            
            response_code = 200
            crc, crc_least_byte, crc_significant_byte = self.__calculate_crc(response_bytes[0:42])
            if crc_least_byte != response_bytes[42] or crc_significant_byte != response_bytes[43]:
                response_code = 403   
                     
            return [response_code, response_bytes]



    def __calculate_crc(cls, byte_list):
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
pass