import time,traceback
import serial_middleware
from devices.bq225 import BQ225
from devices.tescom_SDDPV2200M import Tescom_SDDPV2200M
from devices.growatt_SPF5000ES import Growatt_SPF5000ES
from devices.master_lora import MasterLora
from devices.water_level_simple_slave import water_level_simple_slave


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
def get_BQ225_humidity(BQ225Instance:BQ225, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = BQ225Instance.humidity_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    BQ225Instance.is_valid_humidity_response(response = response)
def get_BQ225_temperature(BQ225Instance:BQ225, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = BQ225Instance.temperature_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    BQ225Instance.is_valid_temperature_response(response = response)

def run_Tescom_SDDPV2200M_driver(Tescom_SDDPV2200MInstance:Tescom_SDDPV2200M, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Tescom_SDDPV2200MInstance.driver_run_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Tescom_SDDPV2200MInstance.is_valid_driver_run_response(response = response)
def stop_Tescom_SDDPV2200M_driver(Tescom_SDDPV2200MInstance:Tescom_SDDPV2200M, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Tescom_SDDPV2200MInstance.driver_stop_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Tescom_SDDPV2200MInstance.is_valid_driver_stop_response(response = response)
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
def get_inverter_pv_power(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Growatt_SPF5000ESInstance.pv_power_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Growatt_SPF5000ESInstance.is_valid_pv_power_response(response = response)
def get_water_level_simple_slave_water_level(SimpleSlaveInstance:water_level_simple_slave, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = SimpleSlaveInstance.water_level_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    SimpleSlaveInstance.is_valid_water_level_response(response = response)


SerialMiddleware = serial_middleware.SerialMiddleware(is_debugging = False)
MasterLora = MasterLora(is_debugging = False)
surec_lab_BQ225 = BQ225(lora_address = 5, slave_address = 141,is_debugging=True, print_humidity = True, print_temperature= True)
machine_laboratory_inverter = Growatt_SPF5000ES(lora_address = 3, slave_address = 16,is_debugging=True , print_BESS_voltage = True, print_load_power= True, print_pv_power= True)
Tescom_SDDPV2200M_1 = Tescom_SDDPV2200M(lora_address = 3, slave_address = 15,is_debugging=True)
water_level_sensor = water_level_simple_slave(lora_address = 3, slave_address = 235,is_debugging=True, print_water_level = True)

while(True):

    try:
        #SETUP
        connect_to_master_device(DEBUG = True, SerialMiddlewareInstance = SerialMiddleware, MasterLoraInstance= MasterLora)
        
        #LOOP
        while(True):
            get_BQ225_temperature(BQ225Instance = surec_lab_BQ225, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
            get_BQ225_humidity(BQ225Instance = surec_lab_BQ225, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
    
            get_inverter_BESS_voltage(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
            get_inverter_load_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
            get_inverter_pv_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
    
            get_water_level_simple_slave_water_level(SimpleSlaveInstance = water_level_sensor, SerialMiddlewareInstance = SerialMiddleware, DEBUG = True)
    except Exception:
        print(traceback.format_exc())
        continue
