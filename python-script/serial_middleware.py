import time,traceback
#https://pyserial.readthedocs.io/en/latest/pyserial.html
import serial, serial.tools.list_ports
import useful_methods

class SerialMiddleware():
    ARDUINO_BOOT_TIME_SECONDS = 5

    def __init__(self, is_debugging = False, baudrate=9600, timeout_seconds=6, byte_size= serial.EIGHTBITS, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE):
        self.py_serial_instance = serial.Serial( baudrate=baudrate, timeout=timeout_seconds, bytesize=byte_size, parity=parity, stopbits=stop_bits)              
        self.IS_DEBUGGING = is_debugging
        self.blocked_ports_list_str = []

    def is_open(self):
        return self.py_serial_instance.is_open
  
    def connect(self, port_name):
        "port_name is a string. Example: 'COM4' or '/dev/ttyUSB0'"
        try:
            if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Connecting to port: " + str(port_name))
            if self.py_serial_instance.is_open:
                self.py_serial_instance.close()
                self.py_serial_instance.port = None    

            self.py_serial_instance.port = port_name
            self.py_serial_instance.open()
            if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Connected to port: " + str(port_name),"Waiting for Arduino to boot...")
            time.sleep(self.ARDUINO_BOOT_TIME_SECONDS)
            return True
        except serial.SerialException:
            print(traceback.format_exc())
            if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Could not connect to port: " + str(port_name))
            if self.py_serial_instance.is_open:
                self.py_serial_instance.close()
            self.py_serial_instance.port = None
            if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Port is freed: " + str(port_name))
            return False

    def disconnect(self):
        if self.py_serial_instance.is_open:
            self.py_serial_instance.close()
        self.py_serial_instance.port = None    

    def get_all_port_names(self):
        ports = list(serial.tools.list_ports.comports())
        port_names_list= []
        for port in ports:
            port_names_list.append(port.device)
        return port_names_list
    
    def is_blocked_port(self, port_name):
        return port_name in self.blocked_ports_list_str
    
    def add_to_blocked_ports(self, port_name=""):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Blocking port: " + str(port_name))
        self.blocked_ports_list_str.append(port_name)

    def remove_from_blocked_ports(self, port_name):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Unblocking port: " + str(port_name))
        self.blocked_ports_list_str.remove(port_name)
    
    def get_blocked_ports(self):
        return self.blocked_ports_list_str
    
    def free_blocked_ports(self):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Freeing blocked ports", self.blocked_ports_list_str)
        self.blocked_ports_list_str = []

    def write_string_to_serial_utf8(self, string_to_write = None):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Writing to serial: " + str(string_to_write))
        self.py_serial_instance.write(string_to_write.encode()) 

    def decorate_and_write_dict_to_serial_utf8(self, request_dict = None):
        request_identifier = request_dict['request_identifier_16']
        command_dict=request_dict['command_dict']
        if request_identifier == None or command_dict == None:raise Exception("request_identifier is None")
        package_bytes = [0]*45
        package_bytes[0]=255 #package status
        package_bytes[1]= request_identifier >> 8 #request identifier significant byte
        package_bytes[2]= request_identifier & 0xFF #request identifier least byte
        package_bytes[3]= command_dict["function_code"] #function code
        package_bytes[4]= command_dict["sub_function_code"] #sub function code
        package_bytes[7]= command_dict["slave_lora_address"]>>8 #slave lora address significant byte
        package_bytes[8]= command_dict["slave_lora_address"]&0xFF #slave lora address least byte
        package_bytes[9]= command_dict["request_data_count"] #request data count
        for i, byte in enumerate(command_dict["request_data_bytes"]):
            package_bytes[10 +i] = byte

        crc_16, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(package_bytes[0:43])
        package_bytes[43] = crc_lst #crc least byte
        package_bytes[44] = crc_sig #crc significant byte

        string_to_write = useful_methods.convert_byte_list_to_string(package_bytes)
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Writing to serial: " + str(string_to_write))
        self.py_serial_instance.write(string_to_write.encode())

    def read_package_from_serial_utf8(self, request_identifier=None):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Reading from serial")
        line = self.py_serial_instance.readline().decode("utf-8")
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Read from serial: " + str(line))
       
        #(0) empty line
        if line =="":
            return [400, None, "Empty line or timeout occured"]
        
        #(1) byte count
        data_bytes_str = line.split(",")
        if len(data_bytes_str) != 45:
            return [402,None, "Number of bytes is not 45, but " + str(len(data_bytes_str)) + ""]
        
        #(2) bytes are integers
        data_bytes_int = []
        try:
            data_bytes_int = [int(byte_str) for byte_str in data_bytes_str]
        except:
            return [403,None, "Not all string bytes are integers"]
        
        #(3) Checksum
        crc_16, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(data_bytes_int[0:43])
        if crc_lst != data_bytes_int[43] or crc_sig != data_bytes_int[44]:
            return [401, None, "Checksum is not valid" ]
        
        #(4) process identifier
        if request_identifier != (data_bytes_int[1]*256+ data_bytes_int[2]):
            return [404, data_bytes_int, "Request and reponse identifiers do not match"]

        #(5) Arduino side errors
        if data_bytes_int[0] != 255:        
            error_dict = {
                43: "Master lora receives corrupted package",
                89: "Master lora receives no reply from slave lora. Either master lora cannot broadcast or slave lora is not responding",
                243: "Master lora receives corrupted reply from slave lora",
                207: "Slave lora receives corrupted package",
                239: "Slave lora receives replies from slave devices connected to it. However, received number of bytes is not proper",
                139:"Slave lora receives no reply from slave devices connected to it",
                1:"Master lora greets the computer",
                2:"Slave lora greets the computer",
                0:"Master receives unknown function and sub function codes",
                86:"Slave lora receives unknown function and sub function codes",   
            }
            if data_bytes_int[0] in error_dict:
                return [data_bytes_int[0], data_bytes_int, error_dict[data_bytes_int[0]]]
            else:
                return [405, data_bytes_int, "Received status code is not defined"]
           
        else:
            return [True, data_bytes_int, "Package is valid"]
      

