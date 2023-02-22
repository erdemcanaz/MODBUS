import serial
import serial.tools.list_ports
import time

def connect_to_device():    
    comport_instances = list(serial.tools.list_ports.comports())
    available_comports_list_str = [comport_instance.device for comport_instance in comport_instances]

    for available_comport in available_comports_list_str:
        try:
            serial_instance = serial.Serial(available_comport, 9600)
            print("Connected to device on port: " + available_comport)
            return serial_instance
        except:
            print("Could not connect to device on port: " + available_comport)
            continue

def write_byte_to_serial(serial_instance, byte_to_write):    
    serial_instance.write(byte_to_write)


serial_instance = connect_to_device()
time.sleep(2)
serial_instance.write("@141,3,2,7,229,10,25\n".encode())
time.sleep(1)
