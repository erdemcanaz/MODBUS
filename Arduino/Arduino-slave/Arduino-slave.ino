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

#define SOFTWARE_SERIAL_CHAR_REGISTER_SIZE 64
#define HARDWARE_SERIAL_CHAR_REGISTER_SIZE 64

#define HARDWARE_SERIAL_BAUD_RATE 9600
#define SOFTWARE_SERIAL_BAUD_RATE 9600
#define WAIT_RESPONSE_TIMEOUT_ms 1000
#define WAIT_RESPONSE_TIME_ms 10

SoftwareSerial s_serial_instance(RX_PIN, TX_PIN);  // Rx,Tx

void setup() {
  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);
  s_serial_instance.begin(SOFTWARE_SERIAL_BAUD_RATE);

  pinMode(RX_PIN, INPUT);
  pinMode(TX_PIN, OUTPUT);

  pinMode(OUT_ENABLE_PIN, OUTPUT);
  digitalWrite(OUT_ENABLE_PIN, LOW);
}

void s_serial_append_new_char_to_write(uint8_t);
void software_serial_write_chars();

void loop() {
  for (uint8_t i = 0; i < 255; i++) {
    s_serial_append_new_char_to_write(i);
    software_serial_write_chars();
    delay(100);
  }
}
