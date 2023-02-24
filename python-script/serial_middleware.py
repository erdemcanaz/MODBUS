import time
#https://pyserial.readthedocs.io/en/latest/pyserial.html
import serial, serial.tools.list_ports

class SerialMiddleware():
    ARDUINO_BOOT_TIME_SECONDS = 3.5

    def __init__(self, baudrate=9600, timeout_seconds=6, byte_size= serial.EIGHTBITS, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE):
        self.py_serial_instance = serial.Serial( baudrate=baudrate, timeout=timeout_seconds, bytesize=byte_size, parity=parity, stopbits=stop_bits)              

        self.blocked_ports_list_str = []

    def is_open(self):
        return self.py_serial_instance.is_open
  
    def connect(self, port_name, DEBUG:bool = False):
        "port_name is a string. Example: 'COM4' or '/dev/ttyUSB0'"
        try:
            if(DEBUG):print("Connecting to port: " + str(port_name))
            self.py_serial_instance.port = port_name
            self.py_serial_instance.open()
            if(DEBUG):print("Connected to port: " + str(port_name),"Waiting for Arduino to boot...")
            time.sleep(self.ARDUINO_BOOT_TIME_SECONDS)
            return True
        except serial.SerialException:
            if(DEBUG):print("Could not connect to port: " + str(port_name))
            if self.py_serial_instance.is_open:
                self.py_serial_instance.close()
            self.py_serial_instance.port = None
            if(DEBUG):print("Port is freed: " + str(port_name))
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
    
    def add_to_blocked_ports(self, port_name="",DEBUG:bool = False):
        if(DEBUG):print("Blocking port: " + str(port_name))
        self.blocked_ports_list_str.append(port_name)

    def remove_from_blocked_ports(self, port_name,DEBUG:bool = False):
        if(DEBUG):print("Unblocking port: " + str(port_name))
        self.blocked_ports_list_str.remove(port_name)
    
    def get_blocked_ports(self):
        return self.blocked_ports_list_str
    
    def free_blocked_ports(self,DEBUG:bool = False):
        if(DEBUG):print("Freeing blocked ports", self.blocked_ports_list_str)
        self.blocked_ports_list_str = []
