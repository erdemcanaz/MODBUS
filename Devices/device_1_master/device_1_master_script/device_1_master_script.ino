#include <SoftwareSerial.h>
#include "config.h"

SoftwareSerial LoraSerial(EBYTE_E32_TX_PIN, EBYTE_E32_RX_PIN);  // software Rx, software Tx

void setup() {
  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);

  configure_ebyte_pins();
  LoraSerial.begin(LORA_SOFTWARE_SERIAL_BAUD_RATE);
  while (!set_ebyte_parameters(EBYTE_PARAMETERS_DEBUG));  
}

void loop() {
  listen_and_execute_valid_computer_orders();
}
