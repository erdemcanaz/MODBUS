#include <SoftwareSerial.h>

bool DEBUG = true;
#define HARDWARE_SERIAL_BAUD_RATE 9600
#define HARDWARE_SERIAL_PREAMBLE 146
#define HARDWARE_SERIAL_WAIT_CHAR_TRANSFER_MS 10

//LORA SETTINGS
#define LORA_SOFTWARE_SERIAL_RX_PIN 2;
#define LORA_SOFTWARE_SERIAL_TX_PIN 3;
SoftwareSerial lora_serial_instance(LORA_SOFTWARE_SERIAL_RX_PIN, LORA_SOFTWARE_SERIAL_TX_PIN);  // Rx,Tx

uint16_t LORA_SOFTWARE_ID = 23;
uint16_t LORA_HARDWARE_ADDRESS = 0;
uint16_t LORA_HARDWARE_CHANNEL = 0;
uint16_t LORA_HARDWARE_BAUD_RATE = 0;
uint16_t LORA_SOFTWARE_SERIAL_BAUD_RATE 9600;


//RS485 SETTINGS
#define RS485_SOFTWARE_SERIAL_RX_PIN 4
#define RS485_SOFTWARE_SERIAL_TX_PIN 5
SoftwareSerial rs485_serial_instance(RS485_SOFTWARE_SERIAL_RX_PIN, RS485_SOFTWARE_SERIAL_TX_PIN);  // Rx,Tx

#define RS485_OUTPUT_ENABLE_PIN 6
uint16_t RS485_SOFTWARE_SERIAL_BAUD_RATE 9600

void setup() {
  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);
  lora_serial_instance.begin(LORA_SOFTWARE_SERIAL_BAUD_RATE);
  rs485_serial_instance.begin(RS485_SOFTWARE_SERIAL_BAUD_RATE);
}

void s_serial_append_new_char_to_write(uint8_t);
void software_serial_write_chars();

void loop() {

  for(int i = 0;i<256;i++){
    s_serial_instance.write(char(0));
    s_serial_instance.write(160);
    s_serial_instance.write(23);    
    s_serial_instance.write(i);
    delay(500);
  }

}
