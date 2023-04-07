#include <SoftwareSerial.h>
#include "config.h"

SoftwareSerial RS485_Serial(RS485_SOFTWARE_SERIAL_RX_PIN, RS485_SOFTWARE_SERIAL_TX_PIN);

void setup() {
  pinMode(water_level_sensor, INPUT);
  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);

  configure_RS485_pins();
  RS485_Serial.begin(RS485_SOFTWARE_SERIAL_BAUD_RATE);
}

void loop() {
  slave_operate();
  calculate_water_sensor_distance_and_save_it_to_input_reg_0();
  delay(500);
}


void calculate_water_sensor_distance_and_save_it_to_input_reg_0() {
  const float max_distance_meters = 15;
  const float voltage_min_volt = 0.4;
  const float voltage_max_volt = 2.0;
  const float voltage_range_volt = 1.6;

  float water_analog_10Bit = analogRead(water_level_sensor);
  float water_analog_voltage = (5 * water_analog_10Bit) / 1023;

  float measured_distance_floating_meters = max_distance_meters * (1 - ((water_analog_voltage - voltage_min_volt) / voltage_range_volt));
  if (measured_distance_floating_meters < 0) {
    measured_distance_floating_meters = 0;
  } else if (measured_distance_floating_meters > 15) {
    measured_distance_floating_meters = 15;
  }
  uint16_t measured_distance_integer_cm = (uint16_t)(measured_distance_floating_meters * 100);
  setter_write_input_register(0,measured_distance_integer_cm);
  if (DEBUG) Serial.println("Meaured distance is: " + String(measured_distance_integer_cm) + " cm");
}

uint16_t getter_read_holding_register(uint8_t holding_register_index) {
  if (holding_register_index >= 0 && holding_register_index < NUMBER_OF_HOLDING_REGISTERS) {
    return holding_registers[holding_register_index];
  } else {
    return 0;
  }
}
uint16_t getter_read_input_register(uint8_t input_register_index) {
  if (input_register_index >= 0 && input_register_index < NUMBER_OF_INPUT_REGISTERS) {
    return input_registers[input_register_index];
  } else {
    return 0;
  }
}
void setter_write_holding_register(uint8_t holding_register_index, uint16_t new_register_value) {
  if (holding_register_index >= 0 && holding_register_index < NUMBER_OF_HOLDING_REGISTERS) {
    holding_registers[holding_register_index] = new_register_value;
  } else {
    return 0;
  }
}
void setter_write_input_register(uint8_t input_register_index, uint16_t new_register_value) {
  if (input_register_index >= 0 && input_register_index < NUMBER_OF_INPUT_REGISTERS) {
    input_registers[input_register_index] = new_register_value;
  } else {
    return 0;
  }
}


