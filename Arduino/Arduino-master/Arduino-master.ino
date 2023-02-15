// MAX487 pinout    ::
// RO (PULLED_UP)   : RX_PIN
// DI               : TX_PIN
//~RE (PULLED_DOWN): OUT_ENABLE_PIN
//  DE (PULLED_DOWN): OUT_ENABLE_PIN
//  Vcc             : 5V
//  GND             : GND

#include <SoftwareSerial.h>

#define DEBUG true
#define RX_PIN 2
#define TX_PIN 3
#define OUT_ENABLE_PIN 4
#define SOFTWARE_SERIAL_BAUD_RATE 9600
#define WAIT_RESPONSE_TIMEOUT_ms 1000
#define WAIT_RESPONSE_TIME_ms 10
SoftwareSerial mySerial(RX_PIN, TX_PIN); // Rx,Tx


void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
