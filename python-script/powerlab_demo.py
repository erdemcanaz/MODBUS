import time,traceback

#import main libraries
import serial_middleware
from devices.master_lora import MasterLora

#import device libraries
from devices.bq225 import BQ225
from devices.tescom_SDDPV2200M import Tescom_SDDPV2200M
from devices.growatt_SPF5000ES import Growatt_SPF5000ES


#device instances
ayasli_sensor = BQ225(lora_address = 5, slave_address = 141,is_debugging=True, print_humidity = True, print_temperature= True)
machine_lab_inverter = Growatt_SPF5000ES(lora_address = 3, slave_address = 16,is_debugging=True , print_BESS_voltage = True, print_load_power= True, print_pv_power= True)

#device functions
def connect_to_master_device(MasterLoraInstance:MasterLora ,SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):    
    if(DEBUG):print(time.strftime("%H:%M:%S", time.localtime()),"Searching for master")

    while(True):
        is_master_found = False

        for comport in SerialMiddlewareInstance.get_all_port_names():
            print(comport)
            time.sleep(1)
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
def get_BQ225_temperature(BQ225Instance:BQ225, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = BQ225Instance.temperature_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    BQ225Instance.is_valid_temperature_response(response = response)
def get_inverter_BESS_voltage(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Growatt_SPF5000ESInstance.BESS_voltage_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Growatt_SPF5000ESInstance.is_valid_BESS_voltage_response(response = response)
def get_inverter_load_power(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Growatt_SPF5000ESInstance.load_power_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Growatt_SPF5000ESInstance.is_valid_load_power_response(response = response)

#Setup
MasterLora = MasterLora(is_debugging = False)
SerialMiddleware = serial_middleware.SerialMiddleware(is_debugging = False)
connect_to_master_device(DEBUG = True, SerialMiddlewareInstance = SerialMiddleware, MasterLoraInstance= MasterLora)

while True:
    get_BQ225_temperature(BQ225Instance = ayasli_sensor, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
    get_inverter_BESS_voltage(Growatt_SPF5000ESInstance = machine_lab_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
    get_inverter_load_power(Growatt_SPF5000ESInstance = machine_lab_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)