//config for device_1_master_script
//PARAMETRIC VARIABLES
#define DEBUG false
#define EBYTE_PARAMETERS_DEBUG false
#define HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS 10 //When hardware serial is not empty, It means there may be data transfer is in progress between master and the computer. This parameter indicates the absolute maximum time for that process to finish
#define LORA_REQUEST_WAIT_REPLY_TIME_MS 3000  //When received package is broadcasted, It takes time to receive the broadcasted data. This parameter indicating that time
#define EBYTE_OPERATION_MODE_CHANGE_DELAY_MS 20 //When MO & M1 pins of the EBYTE is changed, operation mode of the device also changed. In such a case, It takes time to recover from it. This parameter indicating that time

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

#define DEVICE_CHANNEL 12     //0-255
#define DEVICE_ADDRESS 1      //0-65535
#define UART_PARITY_MODE 3    //3->8N1
#define UART_BAUD_MODE 3      //3-> 9600BPS
#define AIR_DATA_RATE_MODE 2  //2-> 2.4Kbps
#define FIXED_TRANSMISSION_MODE 1
#define IO_DRIVE_MODE 1          //1-> TX & AUX: push-pull, RX: pull-up
#define WIRELESS_WAKE_UP_MODE 0  //-> 0.25kbps
#define FEC_MODE 1
#define POWER_MODE 0