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
