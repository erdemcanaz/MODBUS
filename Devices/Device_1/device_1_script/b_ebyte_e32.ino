uint8_t reply_package_buffer[PACKAGE_SIZE_BYTE];

void broadcast_package_and_wait_for_reply() {
  //----------------------------------------------------------
  //[0,1]:[sig-lst]     -> random acces identifier  (2  Byte)
  //[2]                 -> function code            (1  Byte)
  //[3]                 -> sub function code        (1  Byte)
  //[4,5]:[sig-lst]     -> master lora address      (2  Byte)
  //[6,7]:[sig-lst]     -> slave lora address       (2  Byte)
  //[8]                 -> Request data count       (1  Byte)
  //[9:24]:[first-last] -> Request data             (16 Byte)
  //[25]                -> Response data count      (1  Byte)
  //[26:41]:[first-last]-> Response data            (16 Byte)
  //[42,43]:[lst-sig]   -> 16-bit MODBUS CRC        (2  Byte)
  //----------------------------------------------------------

  //SEND REQUEST
  digitalWrite(EBYTE_E32_M0_PIN, LOW);
  digitalWrite(EBYTE_E32_M1_PIN, LOW);

  package_buffer[4] = DEVICE_ADDRESS >> 8;
  package_buffer[5] = DEVICE_ADDRESS % 256;

  uint16_t CRC_calculated = calculate_CRC(true, 0, package_buffer[0]);
  for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
    CRC_calculated = calculate_CRC(false, CRC_calculated, package_buffer[i]);
  }
  package_buffer[42] = CRC_calculated % 256;
  package_buffer[43] = CRC_calculated >> 8;


  //Fixed broadcast
  LoraSerial.write(package_buffer[6]);
  LoraSerial.write(package_buffer[7]);
  LoraSerial.write(DEVICE_CHANNEL);
  //Data
  for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE; i++) {
    LoraSerial.write(package_buffer[i]);
  }

  //GET REPLY
  LoraSerial.listen();
  while (LoraSerial.available()) LoraSerial.read();
  delay(LORA_REQUEST_WAIT_REPLY_TIME_MS);

  if (LoraSerial.available() == 0) {
    if (DEBUG) Serial.println("No reply is received for process(" + String(uint16_t(package_buffer[0])<<8+package_buffer[1]) + ")");
    while (LoraSerial.available()) LoraSerial.read();
    return;
  } else if (LoraSerial.available() != PACKAGE_SIZE_BYTE) {
    if (DEBUG) Serial.println("Number of bytes received as reply do not match with package format -> received bytes:" + String(LoraSerial.available()) + "");
    while (LoraSerial.available()) LoraSerial.read();
    return;
  }

  for(uint8_t i = 0;i<PACKAGE_SIZE_BYTE ;i++){
    reply_package_buffer[i]=LoraSerial.read();
  } 

  //Check whether process identifiers match 
  if(package_buffer[0] == reply_package_buffer[0] && package_buffer[1] == reply_package_buffer[1]){
    if(DEBUG)Serial.println("Reply is received for process("+String(uint16_t(package_buffer[0])<<8+package_buffer[1])+")");
    for(uint8_t i=0;i<PACKAGE_SIZE_BYTE-1;i++){
      Serial.print(String(package_buffer[i])+",");
    } Serial.println(package_buffer[43]);
  }else{
    if(DEBUG)Serial.println("Reply is received but process identifiers do not match");
  }
  while (LoraSerial.available()) LoraSerial.read(); 
}
//----------------------------------------------------------------
uint8_t ebyte_parameters[6];
void configure_ebyte_pins() {
  pinMode(EBYTE_E32_TX_PIN, INPUT);
  pinMode(EBYTE_E32_RX_PIN, OUTPUT);
  pinMode(EBYTE_E32_M0_PIN, OUTPUT);
  pinMode(EBYTE_E32_M1_PIN, OUTPUT);
  pinMode(EBYTE_E32_AUX_PIN, INPUT);
}
void get_ebyte_parameters(bool print_parameters) {

  LoraSerial.listen();
  delay(1000);

  while (LoraSerial.available() > 0) LoraSerial.read();
  digitalWrite(EBYTE_E32_M0_PIN, HIGH);
  digitalWrite(EBYTE_E32_M1_PIN, HIGH);
  delay(100);

  for (uint8_t i = 0; i < 3; i++) LoraSerial.write(193);  //0xC1
  delay(100);

  for (uint8_t i = 0; i < 6; i++) {
    if (LoraSerial.available() == 0) break;
    ebyte_parameters[i] = LoraSerial.read();
  }

  if (print_parameters) {
    Serial.println("--------------------");
    Serial.print("Parameters read:");
    for (uint8_t i = 0; i < 6; i++) Serial.print(String(ebyte_parameters[i]) + ", ");
    Serial.println();
    Serial.println("DEVICE-CHANNEL         :" + String(((ebyte_parameters[4]) & B00011111)));
    Serial.println("DEVICE-ADDRESS         :" + String(uint16_t(ebyte_parameters[1]) * 256 + ebyte_parameters[2]));
    Serial.println("UART-PARITY-MODE       :" + String((ebyte_parameters[3] & B11000000) >> 6));
    Serial.println("UART-BAUD-MODE         :" + String((ebyte_parameters[3] & B00111000) >> 3));
    Serial.println("AIR-DATA-RATE-MODE     :" + String((ebyte_parameters[3] & B00000111)));
    Serial.println("FIXED-TRANSMISSION-MODE:" + String((ebyte_parameters[5] & B10000000) >> 7));
    Serial.println("IO-DRIVE-MODE          :" + String((ebyte_parameters[5] & B01000000) >> 6));
    Serial.println("WIRELESS-WAKE-UP-MODE  :" + String((ebyte_parameters[5] & B00111000) >> 3));
    Serial.println("FEC-MODE               :" + String((ebyte_parameters[5] & B00000100) >> 2));
    Serial.println("POWER-MODE             :" + String((ebyte_parameters[5] & B00000011)));
    Serial.println("--------------------");
  }

  digitalWrite(EBYTE_E32_M0_PIN, LOW);
  digitalWrite(EBYTE_E32_M1_PIN, LOW);
  delay(1000);
}
bool set_ebyte_parameters(bool print_parameters) {
  digitalWrite(EBYTE_E32_M0_PIN, HIGH);
  digitalWrite(EBYTE_E32_M1_PIN, HIGH);
  delay(1000);

  uint8_t parameters[6];
  parameters[0] = 192;  //0xC0
  parameters[1] = DEVICE_ADDRESS >> 8;
  parameters[2] = DEVICE_ADDRESS % 256;
  parameters[3] = (UART_PARITY_MODE & B00000011) << 6;
  parameters[3] += (UART_BAUD_MODE & B00000111) << 3;
  parameters[3] += (AIR_DATA_RATE_MODE & B00000111);
  parameters[4] = (DEVICE_CHANNEL & B00011111);
  parameters[5] = (FIXED_TRANSMISSION_MODE & B00000001) << 7;
  parameters[5] += (IO_DRIVE_MODE & B00000001) << 6;
  parameters[5] += (FEC_MODE & B00000001) << 2;
  parameters[5] += (POWER_MODE & B00000011);

  if (print_parameters) {
    Serial.print("Parameter setting command: ");
    for (uint8_t i = 0; i < 6; i++) Serial.print(String(parameters[i]) + " ");
    Serial.println();
  }

  for (uint8_t i = 0; i < 6; i++) LoraSerial.write(parameters[i]);
  get_ebyte_parameters(print_parameters);

  for (uint8_t i = 0; i < 6; i++) {
    if (ebyte_parameters[i] != parameters[i]) {
      if (DEBUG) Serial.println("Could not set EBYTE_E32 parameters");
      return false;
    }
  }
  if (DEBUG) Serial.println("EBYTE_E32 parameters are set");
  return true;
}
