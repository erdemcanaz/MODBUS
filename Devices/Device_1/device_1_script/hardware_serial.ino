
uint8_t buffer_1[HARDWARE_SERIAL_MAX_PACKAGE_SIZE_BYTE];
uint8_t waiting_byte_count = 0;

void read_hardware_serial() {
  if (Serial.available() == 0) return;
  delay(HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS);

  waiting_byte_count = 0;
  while (Serial.available() > 0) {
    buffer_1[waiting_byte_count] = Serial.parseInt();
    waiting_byte_count += 1;
    if (Serial.peek() == '\n') break;
  }
  while (Serial.available()) Serial.read();


}

bool validate_hardware_serial_package(){
  //----------------------------------------
  //function code       *(1 Byte)
  //Data count          *(1 Byte)
  //Data                 (${Data Count} Byte)
  //CRC least           *(1 Byte)
  //CRC significant     *(1 Byte)
  //----------------------------------------
  if(waiting_byte_count == 0)return false;

  if(waiting_byte_count < 4){
    if(DEBUG)Serial.println("Waiting byte count must be greater than 4, now it is: "+String(waiting_byte_count));
    waiting_byte_count = 0;
    return false;
  }
  
  //Validate CRC  
  uint16_t CRC_expected = calculate_CRC(true, 0, buffer_1[0]);
  for(uint8_t i = 1; i< waiting_byte_count -2; i++){
    CRC_expected = calculate_CRC(false, CRC_expected, buffer_1[i]);
  }
  uint8_t CRC_expected_significant = CRC_expected >>8;
  uint8_t CRC_given_significant = buffer_1[waiting_byte_count -1];
  uint8_t CRC_expected_least = CRC_expected % 256;
  uint8_t CRC_given_least = buffer_1[waiting_byte_count -2];

  if(CRC_expected_significant != CRC_given_significant || CRC_expected_least != CRC_given_least){
    if(DEBUG)Serial.println("Given CRC(lst-sig): "+ String(CRC_given_least)+", "+String(CRC_given_significant)+ " Expected CRC(lst-sig):"+String(CRC_expected_least)+", "+ String(CRC_expected_significant));
    waiting_byte_count = 0;
    return true;
  }
 
  uint8_t data_count = buffer_1[1];
  if(waiting_byte_count != data_count+ 4 ){
    if(DEBUG)Serial.println("Waiting byte count: "+ String(waiting_byte_count)+ " Data count: "+ String(data_count));
    waiting_byte_count = 0;
    return true;
  }
  return true;  
}

void execute_hardware_serial_package(){
  //----------------------------------------
  //function code       *(1 Byte)
  //Data count          *(1 Byte)
  //Data                 (${Data Count} Byte)
  //CRC least           *(1 Byte)
  //CRC significant     *(1 Byte)
  //----------------------------------------
  if(waiting_byte_count == 0)return;

  uint8_t function_code = buffer_1[0];
  uint8_t data_count = buffer_1[1];

  if(function_code == 1){
  //(1) greet computer. This is usefull when there are multiple ports
    Serial.println("Hi, I am here to redirect your MODBUS orders");  
  }
  else if(function_code == 2){
  //(2) get device related parameters

  }
  else if(function_code == 3){
  //(3) set device related parameter

  }
  else if(function_code == 4){
  //(4) Broadcast data package over lora


  }  
  else if(function_code == 5){
  //(5) broadcast data package over rs485

  }  
  else if(function_code == 6){
  //(6) first broadcast data package over rs485, then if no device replies, broadcast it over lora
    
  }
  

  waiting_byte_count = 0;
}





