import time,traceback
import serial_middleware
from devices.bq225 import BQ225
from devices.tescom_SDDPV2200M import Tescom_SDDPV2200M
from devices.growatt_SPF5000ES import Growatt_SPF5000ES
from devices.master_lora import MasterLora
from devices.water_level_simple_slave import water_level_simple_slave
import logger, firebase

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
    return BQ225Instance.is_valid_humidity_response(response = response)
def get_BQ225_temperature(BQ225Instance:BQ225, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = BQ225Instance.temperature_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return BQ225Instance.is_valid_temperature_response(response = response)

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
    return Growatt_SPF5000ESInstance.is_valid_BESS_voltage_response(response = response)
def get_inverter_load_power(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):  
    request_dict = Growatt_SPF5000ESInstance.load_power_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return Growatt_SPF5000ESInstance.is_valid_load_power_response(response = response)
def get_inverter_pv_power(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Growatt_SPF5000ESInstance.pv_power_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return Growatt_SPF5000ESInstance.is_valid_pv_power_response(response = response)
def get_inverter_grid_power(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Growatt_SPF5000ESInstance.grid_power_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return Growatt_SPF5000ESInstance.is_valid_grid_power_response(response = response)
    
def get_water_level_simple_slave_water_level(SimpleSlaveInstance:water_level_simple_slave, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = SimpleSlaveInstance.water_level_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return SimpleSlaveInstance.is_valid_water_level_response(response = response)


SerialMiddleware = serial_middleware.SerialMiddleware(is_debugging = False)
MasterLora = MasterLora(is_debugging = False)
surec_lab_BQ225 = BQ225(lora_address = 5, slave_address = 141,is_debugging=False, print_humidity = False, print_temperature= False)
machine_laboratory_inverter = Growatt_SPF5000ES(lora_address = 3, slave_address = 16,is_debugging=False,print_grid_power= False, print_BESS_voltage= False, print_load_power = False, print_pv_power = False)
Tescom_SDDPV2200M_1 = Tescom_SDDPV2200M(lora_address = 5, slave_address = 15,is_debugging=True)
water_level_sensor = water_level_simple_slave(lora_address = 5, slave_address = 235,is_debugging=False, print_water_level = False)
#dummy_slave = BQ225(lora_address = 4, slave_address = 141,is_debugging=False, print_humidity = False, print_temperature= False)
def measurement_block():
    
    global surec_lab_BQ225, machine_laboratory_inverter, Tescom_SDDPV2200M_1, water_level_sensor, SerialMiddleware, MasterLora
    print("\nmeasurement_block started")
    #Environmental Sensor measurements
    if get_BQ225_humidity(BQ225Instance = surec_lab_BQ225, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("humidity:", surec_lab_BQ225.getter_humidity_percentage())
        logger.append_to_csv_file(operation_tag = "Sensor", device = "BQ225", device_tag = "machine-lab-bq225",tag = "humidity", data = str(surec_lab_BQ225.getter_humidity_percentage()))
        firebase.update_firebase_data(data={"humidity":surec_lab_BQ225.getter_humidity_percentage()})
    else:
        print("humidity: not measured")
        logger.append_to_csv_file(operation_tag = "Sensor", device = "BQ225", device_tag = "machine-lab-bq225", tag = "humidity", data ="ERROR")

    if get_BQ225_temperature(BQ225Instance = surec_lab_BQ225, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("temperature:", surec_lab_BQ225.getter_temperature_celcius())
        logger.append_to_csv_file(operation_tag = "Sensor", device = "BQ225",device_tag = "machine-lab-bq225", tag = "temperature", data =str(surec_lab_BQ225.getter_temperature_celcius()))
        firebase.update_firebase_data(data={"temperature":surec_lab_BQ225.getter_temperature_celcius()})
    else:
        print("temperature: not measured")
        logger.append_to_csv_file(operation_tag = "Sensor", device = "BQ225",device_tag = "machine-lab-bq225", tag = "temperature", data ="ERROR")

    #Inverter related measurements
    all_inverter_measurements_fine = True

    if get_inverter_BESS_voltage(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("BESS voltage:", machine_laboratory_inverter.getter_BESS_voltage())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "BESS-voltage", data =str(machine_laboratory_inverter.getter_BESS_voltage()))
        firebase.update_firebase_data(data={"BESS-voltage":machine_laboratory_inverter.getter_BESS_voltage()})
    else:
        print("BESS voltage: not measured")
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "BESS-voltage", data = "ERROR")
        all_inverter_measurements_fine = False

    if get_inverter_load_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("load power:", machine_laboratory_inverter.getter_load_power())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES", device_tag = "machine-lab-inverter", tag = "load-power", data =str(machine_laboratory_inverter.getter_load_power()))
        firebase.update_firebase_data(data={"load-power":machine_laboratory_inverter.getter_load_power()})
    else:
        print("load power: not measured")
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "load-power", data = "ERROR")
        all_inverter_measurements_fine = False
    
    if get_inverter_pv_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("pv power:", machine_laboratory_inverter.getter_pv_power())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES", device_tag = "machine-lab-inverter", tag = "pv-power", data =str(machine_laboratory_inverter.getter_pv_power()))
        firebase.update_firebase_data(data={"pv-power":machine_laboratory_inverter.getter_pv_power()})

    else:
        print("pv power: not measured")
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES", device_tag = "machine-lab-inverter", tag = "pv-power", data = "ERROR")
        all_inverter_measurements_fine = False
    
    if get_inverter_grid_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("grid power:", machine_laboratory_inverter.getter_grid_power())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "grid-power", data =str(machine_laboratory_inverter.getter_grid_power()))
        firebase.update_firebase_data(data={"grid-power":machine_laboratory_inverter.getter_grid_power()})

    else:
        print("grid power: not measured")
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES", device_tag = "machine-lab-inverter", tag = "grid-power", data = "ERROR")
        all_inverter_measurements_fine = False
    
    if all_inverter_measurements_fine:
        print("all measurements fine")
        print("BESS power (calculated): ", machine_laboratory_inverter.calculate_BESS_power())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "calculated-BESS-power", data =str(machine_laboratory_inverter.calculate_BESS_power()))
        print("BESS current (calculated): ", machine_laboratory_inverter.calculate_BESS_current())
        logger.append_to_csv_file(operation_tag = "Inverter", device = "GROWATT_SPF5000_ES",device_tag = "machine-lab-inverter", tag = "calculated-BESS-current", data =str(machine_laboratory_inverter.calculate_BESS_current()))
        print("BESS state of charge (calculated): ", machine_laboratory_inverter.calculate_BESS_state_of_charge())

    #Water level sensor
    if get_water_level_simple_slave_water_level(SimpleSlaveInstance = water_level_sensor, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False):
        print("water level:", water_level_sensor.getter_water_level())
        logger.append_to_csv_file(operation_tag = "Sensor", device = "Nivelco-waterlevel",device_tag = "machine-lab-water-level", tag = "water-level", data =str(water_level_sensor.getter_water_level()))
        firebase.update_firebase_data(data={"water-level":water_level_sensor.getter_water_level()})
    else:
        print("water level: not measured")
        logger.append_to_csv_file(operation_tag = "Sensor", device = "Nivelco-waterlevel",device_tag = "machine-lab-water-level", tag = "water-level", data = "ERROR")

while(True):

    try:
        #SETUP
        connect_to_master_device(DEBUG = False, SerialMiddlewareInstance = SerialMiddleware, MasterLoraInstance= MasterLora)
        
        #LOOP
        while(True):
            measurement_block()
            #get_BQ225_humidity(BQ225Instance= dummy_slave , SerialMiddlewareInstance= SerialMiddleware, DEBUG= True)


    except Exception:
        print(traceback.format_exc())
        continue

