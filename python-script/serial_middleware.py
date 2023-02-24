import time
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
            self.py_serial_instance.port = port_name
            self.py_serial_instance.open()
            if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Connected to port: " + str(port_name),"Waiting for Arduino to boot...")
            time.sleep(self.ARDUINO_BOOT_TIME_SECONDS)
            return True
        except serial.SerialException:
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

    def read_package_from_serial_utf8(self, request_identifier=None):
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Reading from serial")
        line = self.py_serial_instance.readline().decode("utf-8")
        if(self.IS_DEBUGGING):print(time.strftime("%H:%M:%S", time.localtime()),"Read from serial: " + str(line))
       
        #(0) empty line
        if line =="":
            return [400, None]
        
        #(1) byte count
        data_bytes_str = line.split(",")
        if len(data_bytes_str) != 45:
            return [402,None]
        
        #(2) bytes are integers
        data_bytes_int = []
        try:
            data_bytes_int = [int(byte_str) for byte_str in data_bytes_str]
        except:
            return [403,None]
        
        #(3) Checksum
        crc_16, crc_lst, crc_sig = useful_methods.calculate_crc_for_bytes_list(data_bytes_int[0:43])
        if crc_lst != data_bytes_int[43] or crc_sig != data_bytes_int[44]:
            return [401, None]
        
        #(4) process identifier
        if request_identifier != (data_bytes_int[1]*256+ data_bytes_int[2]):
            return [404, data_bytes_int]

        #return package 
        return [True, data_bytes_int]
      

