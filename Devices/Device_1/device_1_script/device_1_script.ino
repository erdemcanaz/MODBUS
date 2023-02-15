#include <SoftwareSerial.h>

bool DEBUG = true;
#define HARDWARE_SERIAL_BAUD_RATE 9600
#define HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS 10  //must be greater than ->  { 1000 * (1/baudrate) * HARDWARE_SERIAL_MAX_PACKAGE_SIZE_BYTE }
#define HARDWARE_SERIAL_MAX_PACKAGE_SIZE_BYTE 100

//LORA SETTINGS
#define LORA_MAX_PACKAGE_SIZE 32
#define LORA_SOFTWARE_SERIAL_BAUD_RATE 9600

#define EBYTE_M0_PIN 2
#define EBYTE_M1_PIN 3
#define EBYTE_TX_PIN 4  //Software serial RX
#define EBYTE_RX_PIN 5  //Software serial TX
#define EBYTE_AUX_PIN 6

#define EBYTE_DELAY_MS 50
#define EBYTE_HARDWARE_ADDRESS 0
#define EBYTE_HARDWARE_CHANNEL 0
#define EBYTE_AIR_DATA_RATE_MODE 0
#define EBYTE_TRANSMISSION_POWER_MODE 0
#define EBYTE_BAUD_RATE_MODE 0
#define EBYTE_UART_CONFIG_MODE 0
#define EBYTE_FEC_MODE 0
#define EBYTE_FIXED_TRANSMISSION_MODE 0
#define EBYTE_WAKE_UP_TIME_MODE 0
#define EBYTE_IO_DRIVE_MODE 0

//RS485 SETTINGS (8N1)
#define RS485_SOFTWARE_SERIAL_RX_PIN 7
#define RS485_SOFTWARE_SERIAL_TX_PIN 8
#define RS485_OUTPUT_ENABLE_PIN 9
#define RS485_SOFTWARE_SERIAL_BAUD_RATE 9600

//----------------------------------------------------------------------------
uint16_t calculate_CRC(bool, uint16_t, uint16_t);
SoftwareSerial lora_serial_instance(EBYTE_TX_PIN, EBYTE_RX_PIN);  // software Rx, software Tx
SoftwareSerial rs485_serial_instance(RS485_SOFTWARE_SERIAL_RX_PIN, RS485_SOFTWARE_SERIAL_TX_PIN);  // Rx,Tx

void setup() {
  configure_ebyte_pins();

  Serial.begin(HARDWARE_SERIAL_BAUD_RATE);
  lora_serial_instance.begin(LORA_SOFTWARE_SERIAL_BAUD_RATE);
  rs485_serial_instance.begin(RS485_SOFTWARE_SERIAL_BAUD_RATE);

}

void loop() {
  read_hardware_serial();
  validate_hardware_serial_package();
  execute_hardware_serial_package();

  get_ebyte_parameters(true);

  delay(5000);
}
