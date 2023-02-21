
//----------------------------------------------------------------
uint8_t ebyte_parameters[6];
void configure_ebyte_pins() {
  pinMode(EBYTE_TX_PIN, INPUT);
  pinMode(EBYTE_RX_PIN, OUTPUT);
  pinMode(EBYTE_M0_PIN, OUTPUT);
  pinMode(EBYTE_M1_PIN, OUTPUT);
  pinMode(EBYTE_AUX_PIN, INPUT);
}
void get_ebyte_parameters(bool print_parameters) {

  lora_serial_instance.listen();
  delay(1000);    

  while (lora_serial_instance.available() > 0) lora_serial_instance.read();
  digitalWrite(EBYTE_M0_PIN, HIGH);
  digitalWrite(EBYTE_M1_PIN, HIGH);
  delay(100);

  for (uint8_t i = 0; i < 3; i++) lora_serial_instance.write(193);  //0xC1
  delay(100);

  for (uint8_t i = 0; i < 6; i++) {
    if (lora_serial_instance.available() == 0) break;
    ebyte_parameters[i] = lora_serial_instance.read();
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

  digitalWrite(EBYTE_M0_PIN, LOW);
  digitalWrite(EBYTE_M1_PIN, LOW);
  delay(1000);
  
}
bool set_ebyte_parameters(bool print_parameters) {
  digitalWrite(EBYTE_M0_PIN, HIGH);
  digitalWrite(EBYTE_M1_PIN, HIGH);
  delay(1000);

  uint8_t parameters[6];
  parameters[0] = 192;  //0xC0
  parameters[1] = DEVICE_ADDRESS >> 8;
  parameters[2] = DEVICE_ADDRESS % 256;
  parameters[3] = (UART_PARITY_MODE & B00000011) << 6;
  parameters[3] += (UART_BAUD_MODE & B00000111) << 3;
  parameters[3] += (AIR_DATA_RATE_MODE & B00000111);
  parameters[4] = (DEVICE_CHANNEL & B00011111);
  parameters[5] = (FIXED_TRANSMISSION_MODE& B00000001)<<7;
  parameters[5] += (IO_DRIVE_MODE& B00000001)<<6;
  parameters[5] += (FEC_MODE& B00000001)<<2;
  parameters[5] += (POWER_MODE& B00000011);

  if(print_parameters){
    Serial.print("Parameter setting command: ");
    for(uint8_t i=0;i<6;i++)Serial.print(String(parameters[i])+" ");
    Serial.println();
  }
  
  for(uint8_t i = 0; i <6; i++)lora_serial_instance.write(parameters[i]);
  get_ebyte_parameters(print_parameters);

  for(uint8_t i = 0; i <6; i++){
    if(ebyte_parameters[i]!=parameters[i]){
      if(DEBUG) Serial.println("Could not set EBYTE parameters");      
      return false;
    }
  }
  if(DEBUG)Serial.println("EBYTE parameters are set");
  return true;
}
