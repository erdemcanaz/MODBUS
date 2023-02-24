import serial_middleware
import time 
from devices.bq225 import BQ225
from devices.master_lora import MasterLora

def connect_to_master_device(MasterLoraInstance:MasterLora ,SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):    
    while(True):
        is_master_found = False

        for comport in SerialMiddlewareInstance.get_all_port_names():

            if not SerialMiddlewareInstance.is_blocked_port(comport):
                if SerialMiddlewareInstance.connect(comport): 
                    request = MasterLora.greet_request_str() #[${request_identifier}, ${request package as string}]
                    SerialMiddlewareInstance.write_string_to_serial_utf8(string_to_write = request[1])
                    response= SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request[0])
                    if(MasterLora.is_valid_greeting_response(response = response)):
                        is_master_found = True
                        break           
                else:
                    SerialMiddlewareInstance.add_to_blocked_ports(comport)
                    continue                         
                                        
        if is_master_found:
            if(DEBUG):print(time.strftime("%H:%M:%S", time.localtime()),"Master found at port: " + comport)
            break
        else:
            SerialMiddlewareInstance.free_blocked_ports()


MasterLora = MasterLora(is_debugging = True)
SerialMiddleware = serial_middleware.SerialMiddleware(is_debugging = True)

while(True):
    connect_to_master_device(DEBUG = True, SerialMiddlewareInstance = SerialMiddleware, MasterLoraInstance= MasterLora)
    while(True):
        time.sleep(1)
