import time,traceback
import serial_middleware, pprint
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
def get_Tescom_SDDPV2200M_driver_VFD_frequency(Tescom_SDDPV2200MInstance:Tescom_SDDPV2200M, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
        request_dict = Tescom_SDDPV2200MInstance.get_Tescom_SDDPV2200M_driver_VFD_frequency_dict() 
        SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
        response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
        return Tescom_SDDPV2200MInstance.is_valid_get_Tescom_SDDPV2200M_driver_VFD_frequency_response(response = response)
def get_Tescom_SDDPV2200M_driver_VFD_voltage(Tescom_SDDPV2200MInstance:Tescom_SDDPV2200M, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = Tescom_SDDPV2200MInstance.get_Tescom_SDDPV2200M_DC_voltage() 
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Tescom_SDDPV2200MInstance.is_valid_get_Tescom_SDDPV2200M_DC_voltage_response(response = response)
def set_Tescom_SDDPV2200M_driver_reference_voltage(Tescom_SDDPV2200MInstance:Tescom_SDDPV2200M, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False, reference_voltage = None):
    request_dict = Tescom_SDDPV2200MInstance.set_driver_reference_voltage_dict(reference_voltage= reference_voltage)
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Tescom_SDDPV2200MInstance.is_valid_driver_reference_voltage_response(response = response)

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
def set_inverter_charging_current(Growatt_SPF5000ESInstance:Growatt_SPF5000ES, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, charging_current:float, DEBUG:bool = False, ):
    request_dict = Growatt_SPF5000ESInstance.set_inverter_charging_current_dict(charging_current = charging_current)
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    Growatt_SPF5000ESInstance.is_valid_set_inverter_charging_current_response(response = response)

def get_water_level_simple_slave_water_level(SimpleSlaveInstance:water_level_simple_slave, SerialMiddlewareInstance:serial_middleware.SerialMiddleware, DEBUG:bool = False):
    request_dict = SimpleSlaveInstance.water_level_request_dict()
    SerialMiddlewareInstance.decorate_and_write_dict_to_serial_utf8(request_dict = request_dict)
    response = SerialMiddlewareInstance.read_package_from_serial_utf8(request_identifier = request_dict["request_identifier_16"])
    return SimpleSlaveInstance.is_valid_water_level_response(response = response)

SerialMiddleware = serial_middleware.SerialMiddleware(is_debugging = False)
MasterLora = MasterLora(is_debugging = False)
surec_lab_BQ225 = BQ225(lora_address = 30, slave_address = 141,is_debugging=False, print_humidity = False, print_temperature= False)
machine_laboratory_inverter = Growatt_SPF5000ES(lora_address = 10, slave_address = 16,is_debugging=True,print_grid_power= True, print_BESS_voltage= True, print_load_power = True, print_pv_power = True)
Tescom_SDDPV2200M_1 = Tescom_SDDPV2200M(lora_address = 30, slave_address = 15,is_debugging=True)
water_level_sensor = water_level_simple_slave(lora_address = 5, slave_address = 235,is_debugging=False, print_water_level = False)

#======================================================================================================================================================================

system_variables = {           
            "inverter":{

                    "BESS_voltage":None, #V
                    "BESS_voltage_last_time_updated":time.time(),
                    "load_power":None,  #W
                    "load_power_last_time_updated":time.time(),
                    "pv_power":None, #W
                    "pv_power_last_time_updated":time.time(),
                    "grid_power":None, #W
                    "grid_power_last_time_updated":time.time(),

                    "BESS_charging_current":None, #A
                    "BESS_charging_current_last_time_updated":time.time(),
                    "desired_BESS_charging_current":None, #A
                    "desired_BESS_charging_current_last_time_updated":time.time(),

                    "calculated_BESS_power":None, #W
                    "calculated_BESS_power_last_time_updated":time.time(),
                    "calculated_BESS_current":None, #A
                    "calculated_BESS_current_last_time_updated":time.time(),

            },
             "VFD":{
                "mode":None, #1:run, 5: stop
                "mode_last_time_updated":time.time(),

                "reference_voltage":None, #V
                "reference_voltage_last_time_updated":time.time(),
                "desired_reference_voltage":None, #V
                "desired_reference_voltage_last_time_updated":time.time(),

                "DC_line_voltage":None, #V
                "DC_line_voltage_last_time_updated":time.time(),

                "VFD_frequency":None, #Hz            
                "VFD_frequency_last_time_updated":time.time(),
                "desired_VFD_frequency":None, #Hz
                "desired_VFD_frequency_last_time_updated":time.time(),
                
            }
        }

def setup_block():
    #set initial inverter charging current as 50
    system_variables["inverter"]["desired_BESS_charging_current"] = 0
    system_variables["inverter"]["desired_BESS_charging_current_last_time_updated"] = time.time()
    #set initial VFD reference frequency as 0
    system_variables["VFD"]["desired_VFD_frequency"] = 0
    system_variables["VFD"]["desired_VFD_frequency_last_time_updated"] = time.time()

    #be sure that motor is stopped
    stop_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["VFD"]["mode"] = 5
    system_variables["VFD"]["mode_last_time_updated"] = time.time()

    time.sleep(1)

    set_inverter_charging_current(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, charging_current = system_variables["inverter"]["desired_BESS_charging_current"], DEBUG = False)
    system_variables["inverter"]["BESS_charging_current"] = system_variables["inverter"]["desired_BESS_charging_current"]
    system_variables["inverter"]["BESS_charging_current_last_time_updated"] = time.time()

def measurement_block():
    ##VFD
    get_Tescom_SDDPV2200M_driver_VFD_voltage(Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["VFD"]["DC_line_voltage"] = Tescom_SDDPV2200M_1.getter_DC_voltage()
    system_variables["VFD"]["DC_line_voltage_last_time_updated"] = time.time()

    get_Tescom_SDDPV2200M_driver_VFD_frequency(Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["VFD"]["VFD_frequency"] = Tescom_SDDPV2200M_1.getter_VFD_frequency()
    system_variables["VFD"]["VFD_frequency_last_time_updated"] = time.time()   

    ##inverter
    get_inverter_BESS_voltage(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["inverter"]["BESS_voltage"] = machine_laboratory_inverter.getter_BESS_voltage()
    system_variables["inverter"]["BESS_voltage_last_time_updated"] = time.time()

    get_inverter_load_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["inverter"]["load_power"] = machine_laboratory_inverter.getter_load_power()
    system_variables["inverter"]["load_power_last_time_updated"] = time.time()

    get_inverter_pv_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["inverter"]["pv_power"] = machine_laboratory_inverter.getter_pv_power()
    system_variables["inverter"]["pv_power_last_time_updated"] = time.time()

    get_inverter_grid_power(Growatt_SPF5000ESInstance = machine_laboratory_inverter, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
    system_variables["inverter"]["grid_power"] = machine_laboratory_inverter.getter_grid_power()
    system_variables["inverter"]["grid_power_last_time_updated"] = time.time()

    system_variables["inverter"]["calculated_BESS_power"] = machine_laboratory_inverter.calculate_BESS_power()
    system_variables["inverter"]["calculated_BESS_power_last_time_updated"] = time.time()

    system_variables["inverter"]["calculated_BESS_current"] = machine_laboratory_inverter.calculate_BESS_current()
    system_variables["inverter"]["calculated_BESS_current_last_time_updated"] = time.time()

def run_motor_at_frequency(tescom_VFD_object= None, serial_middleware_object = None, desired_frequency= None):
        #desired frequency is in Hz
        get_Tescom_SDDPV2200M_driver_VFD_voltage(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
        VFD_voltage_initial = tescom_VFD_object.getter_DC_voltage()
        get_Tescom_SDDPV2200M_driver_VFD_frequency(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
        VFD_frequency_initial = tescom_VFD_object.getter_VFD_frequency()
        
        if (desired_frequency <= 0):
            stop_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
            print("VFD stopped")
            return None
        else:
            run_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
            print("VFD running")


        delta_voltage = min(20, (100/(VFD_frequency_initial+0.01)))
        transient_time = 40 if (VFD_frequency_initial < 15) else 5
        recovery_time = 20

        if desired_frequency >= 50 and VFD_frequency_initial >49.5:
            return None
        elif desired_frequency>VFD_frequency_initial:
            delta_voltage = -delta_voltage
        elif desired_frequency<VFD_frequency_initial:
            delta_voltage = delta_voltage

        VFD_voltage_candidate = VFD_voltage_initial + delta_voltage
        set_Tescom_SDDPV2200M_driver_reference_voltage(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, reference_voltage = VFD_voltage_candidate)
        print("VFD reference voltage set to: " + str(VFD_voltage_candidate) + " V")

        time.sleep(transient_time)        
        get_Tescom_SDDPV2200M_driver_VFD_frequency(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
        VFD_frequency_now = tescom_VFD_object.getter_VFD_frequency()
        get_Tescom_SDDPV2200M_driver_VFD_voltage(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, DEBUG = False)
        VFD_voltage_now = tescom_VFD_object.getter_DC_voltage()

        print("VFD frequency now: " + str(VFD_frequency_now) + " Hz")
        print("VFD voltage now: " + str(VFD_voltage_now) + " V")        

        if(abs(VFD_voltage_now-VFD_voltage_candidate)>12 and False):#impulse check
            set_Tescom_SDDPV2200M_driver_reference_voltage(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, reference_voltage = int(VFD_voltage_now))
            print("impulse detected, VFD reference voltage set to: " + str(VFD_voltage_now) + " V")
            time.sleep(recovery_time)
        elif( abs(desired_frequency-VFD_frequency_now) < abs(desired_frequency-VFD_frequency_initial)): #correct decision
            print("correct decision, frequency changed from: " + str(VFD_frequency_initial) + " Hz to " + str(VFD_frequency_now) + " Hz")
            return None
        elif( abs(desired_frequency-VFD_frequency_now) > abs(desired_frequency-VFD_frequency_initial)):#wrong decision            
            VFD_voltage_candidate = VFD_voltage_initial - (2*delta_voltage)
            set_Tescom_SDDPV2200M_driver_reference_voltage(Tescom_SDDPV2200MInstance = tescom_VFD_object, SerialMiddlewareInstance = serial_middleware_object, reference_voltage = VFD_voltage_candidate)
            print("wrong decision, VFD reference voltage set to: " + str(VFD_voltage_candidate) + " V")
            time.sleep(recovery_time)    
        else:
            pass     
       
while(True):

    try:
        #SETUP
        connect_to_master_device(DEBUG = False, SerialMiddlewareInstance = SerialMiddleware, MasterLoraInstance= MasterLora)

        #run_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
        #stop_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)

        setup_block()

        #LOOP
        while(True):
            pass
            #run_motor_at_frequency(tescom_VFD_object= Tescom_SDDPV2200M_1, serial_middleware_object = SerialMiddleware, desired_frequency= 50)
        
            #run_Tescom_SDDPV2200M_driver( Tescom_SDDPV2200MInstance = Tescom_SDDPV2200M_1, SerialMiddlewareInstance = SerialMiddleware, DEBUG = False)
            measurement_block()
           
            
            


    except Exception:
        print(traceback.format_exc())
        continue