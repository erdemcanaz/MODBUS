#include <SoftwareSerial.h>
#include "config.h"

SoftwareSerial RS485_Serial(RS485_SOFTWARE_SERIAL_RX_PIN, RS485_SOFTWARE_SERIAL_TX_PIN);

void setup() {
  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);

  configure_RS485_pins();
  RS485_Serial.begin(RS485_SOFTWARE_SERIAL_BAUD_RATE);

}

void loop() {
  slave_operate();
}

uint16_t getter_read_holding_register(uint8_t holding_register_index){
  if(holding_register_index >= 0 && holding_register_index < NUMBER_OF_HOLDING_REGISTERS){
    return holding_registers[holding_register_index];
  }else{
    return 0;
  }
}
uint16_t getter_read_input_register(uint8_t input_register_index){
  if(input_register_index >= 0 && input_register_index < NUMBER_OF_INPUT_REGISTERS){
    return input_registers[input_register_index];
  }else{
    return 0;
  }
}
void setter_write_holding_register(uint8_t holding_register_index, uint16_t new_register_value){
  if(holding_register_index >= 0 && holding_register_index < NUMBER_OF_HOLDING_REGISTERS){
    holding_registers[holding_register_index] =  new_register_value;
  }else{
    return 0;
  }
}



