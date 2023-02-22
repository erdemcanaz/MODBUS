#include <SoftwareSerial.h>

//SOFTWARE RELATED STATIC VARIABLES
#define PACKAGE_SIZE_BYTE 44
#define HARDWARE_SERIAL_BAUD_RATE 9600
#define LORA_SOFTWARE_SERIAL_BAUD_RATE 9600
#define RS485_SOFTWARE_SERIAL_BAUD_RATE 9600

//HARDWARE RELATED STATIC VARIABLES
#define RS485_SOFTWARE_SERIAL_RX_PIN 7
#define RS485_SOFTWARE_SERIAL_TX_PIN 8
#define RS485_OUTPUT_ENABLE_PIN 9

#define EBYTE_E32_M0_PIN 2
#define EBYTE_E32_M1_PIN 3
#define EBYTE_E32_TX_PIN 4  //Software serial RX
#define EBYTE_E32_RX_PIN 5  //Software serial TX
#define EBYTE_E32_AUX_PIN 6

#define DEVICE_CHANNEL 12  //0-255
#define DEVICE_ADDRESS 1 //0-65535
#define UART_PARITY_MODE 3 //3->8N1
#define UART_BAUD_MODE 3 //3-> 9600BPS
#define AIR_DATA_RATE_MODE 2 //2-> 2.4Kbps
#define FIXED_TRANSMISSION_MODE 1
#define IO_DRIVE_MODE 1 //1-> TX & AUX: push-pull, RX: pull-up
#define WIRELESS_WAKE_UP_MODE 0 //0-> 0.25kbps
#define FEC_MODE 1
#define POWER_MODE 0

//PARAMETRIC VARIABLES
#define DEBUG true
#define HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS 10 
#define LORA_REQUEST_WAIT_REPLY_TIME_MS 1000

//----------------------------------------------------------------------------
SoftwareSerial LoraSerial(EBYTE_E32_TX_PIN, EBYTE_E32_RX_PIN);  // software Rx, software Tx

void setup() {
  configure_ebyte_pins();

  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);
  LoraSerial.begin(LORA_SOFTWARE_SERIAL_BAUD_RATE);

  while(!set_ebyte_parameters(false));
}

void loop() {
  listen_and_execute_valid_computer_orders();
}

uint16_t calculate_CRC(bool is_first_data, uint16_t previously_calculated_crc, uint16_t new_byte){ 
  uint16_t key = 40961; // 1010 0000 0000 0001
  if(is_first_data == true)previously_calculated_crc = 65535; //0xFFFF

  new_byte = new_byte ^ previously_calculated_crc;
  
  for (int i = 0; i < 8; i++)
  {
    bool should_XOR = false;
    if (new_byte % 2 == 1)
      should_XOR = true;
    new_byte = new_byte >> 1;
    if (should_XOR)
      new_byte = new_byte ^ key;
  }
  return new_byte;
}


