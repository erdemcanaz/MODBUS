import modbus_devices.BQ225 as BQ225
import serial_middleware
import time 


def connect_to_master_device(SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):    
    while(True):
        is_master_found = False

        for comport in SerialMiddlewareInstance.get_all_port_names():
            if SerialMiddlewareInstance.is_blocked_port(comport):
                if(DEBUG):print("Port is in blocked ports: " + comport)
                time.sleep(1)
            else: 
                is_master_found = SerialMiddlewareInstance.connect(comport,DEBUG=DEBUG)
                if(DEBUG):print("Connected to: " + comport)
                SerialMiddlewareInstance.disconnect()
                SerialMiddlewareInstance.add_to_blocked_ports(comport,DEBUG=DEBUG)
                is_master_found = False
        
        SerialMiddlewareInstance.free_blocked_ports(DEBUG=DEBUG)
        if is_master_found:
            if(DEBUG):print("Master found at port: " + comport)
            break



SerialMiddlewareInstance = serial_middleware.SerialMiddleware()
while(True):
    connect_to_master_device(DEBUG = True, SerialMiddlewareInstance = SerialMiddlewareInstance)
    pass
