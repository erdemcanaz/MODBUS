//config for device_1_slave_script
//PARAMETRIC VARIABLES
#define DEBUG true
#define EBYTE_PARAMETERS_DEBUG true
#define LORA_WAIT_DATA_TRANSFER_MS 500
#define RS485_REQUEST_WAIT_REPLY_TIME_MS 100
#define EBYTE_OPERATION_MODE_CHANGE_DELAY_MS 50 //When MO & M1 pins of the EBYTE is changed, operation mode of the device also changed. In such a case, It takes time to recover from it. This parameter indicating that time

//SOFTWARE RELATED STATIC VARIABLES
#define PACKAGE_SIZE_BYTE 45
#define DATA_SIZE_BYTE 16
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
#define DEVICE_ADDRESS 8 //0-65535
#define UART_PARITY_MODE 3 //3->8N1
#define UART_BAUD_MODE 3 //3-> 9600BPS
#define AIR_DATA_RATE_MODE 2 //2-> 2.4Kbps
#define FIXED_TRANSMISSION_MODE 1
#define IO_DRIVE_MODE 1 //1-> TX & AUX: push-pull, RX: pull-up
#define WIRELESS_WAKE_UP_MODE 0 //0-> 0.25kbps
#define FEC_MODE 1
#define POWER_MODE 0

void configure_RS485_pins();
void configure_ebyte_pins();
bool set_ebyte_parameters(bool);
uint16_t calculate_CRC(bool , uint16_t , uint16_t );