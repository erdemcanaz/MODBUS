//config for device_1_master_script
//PARAMETRIC VARIABLES
#define DEBUG true

//SOFTWARE RELATED STATIC VARIABLES
#define HARDWARE_SERIAL_BAUD_RATE 9600
#define RS485_SOFTWARE_SERIAL_BAUD_RATE 9600
#define RS485_SLAVE_ID 235
#define NUMBER_OF_HOLDING_REGISTERS 16 // FC:3
#define NUMBER_OF_INPUT_REGISTERS 16 //FC:4
#define WAIT_RS485_TIME_ms 10

//HARDWARE RELATED STATIC VARIABLES
#define RS485_SOFTWARE_SERIAL_RX_PIN 7
#define RS485_SOFTWARE_SERIAL_TX_PIN 8
#define RS485_OUTPUT_ENABLE_PIN 9