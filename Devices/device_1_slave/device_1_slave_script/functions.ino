//Functions for device_1_slave_script
uint8_t request_package_buffer[PACKAGE_SIZE_BYTE];

void listen_and_execute_valid_master_lora_orders() {
  if (!LoraSerial.isListening()) LoraSerial.listen();
  if (LoraSerial.available() == 0) return;

  //(1)______________________________________________________________________________________________________________
  delay(LORA_WAIT_DATA_TRANSFER_MS);
  uint8_t received_byte_count = 0;
  while (LoraSerial.available() > 0) {
    request_package_buffer[received_byte_count] = LoraSerial.read();
    received_byte_count += 1;
    if (received_byte_count >= PACKAGE_SIZE_BYTE) break;
  }
  while (LoraSerial.available() > 0) LoraSerial.read();

  //(2)______________________________________________________________________________________________________________
  bool is_received_byte_count_correct = received_byte_count == PACKAGE_SIZE_BYTE;
  bool is_received_CRC_correct = true;

  uint16_t CRC_calculated = calculate_CRC(true, 0, request_package_buffer[0]);
  for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
    CRC_calculated = calculate_CRC(false, CRC_calculated, request_package_buffer[i]);
  }
  is_received_CRC_correct = ((CRC_calculated >> 8) == request_package_buffer[PACKAGE_SIZE_BYTE - 1]) && ((CRC_calculated % 256) == request_package_buffer[PACKAGE_SIZE_BYTE - 2]);

  if (!is_received_byte_count_correct || !is_received_CRC_correct) {
    if (DEBUG && !is_received_byte_count_correct) Serial.println("Received byte count is not enough, it is: " + String(received_byte_count));
    else if (DEBUG && !is_received_CRC_correct) Serial.println("Received CRC(lst-sig):" + String(request_package_buffer[PACKAGE_SIZE_BYTE - 2]) + "," + String(request_package_buffer[PACKAGE_SIZE_BYTE - 1]) + ". However True CRC(lst-sig):" + String((CRC_calculated % 256)) + "," + String((CRC_calculated >> 8)));
    //TODO: master lora data package is received but it is corrupted
    Serial.println("STATUS-404");
    return;
  }

  //(3)______________________________________________________________________________________________________________
  if (request_package_buffer[2] == 1 && request_package_buffer[3] == 99) { ; }  //greet_master
  else if (request_package_buffer[2] == 1 && request_package_buffer[3] == 0) {

    if(!RS485_Serial.isListening())RS485_Serial.listen();
    while (RS485_Serial.available() > 0) RS485_Serial.read();
    for (uint8_t i = 0; i < DATA_SIZE_BYTE; i++) request_package_buffer[26 + i] = 0;

    digitalWrite(RS485_OUTPUT_ENABLE_PIN, HIGH);
    for (uint8_t i = 0; i < request_package_buffer[8]; i++) {
      RS485_Serial.write(request_package_buffer[9 + i]);
    }
    digitalWrite(RS485_OUTPUT_ENABLE_PIN, LOW);

    delay(RS485_REQUEST_WAIT_REPLY_TIME_MS);
    uint8_t response_data_count = RS485_Serial.available();

    if (response_data_count > DATA_SIZE_BYTE) response_data_count = DATA_SIZE_BYTE;//TODO:add error 405
    else if (response_data_count == 0) response_data_count = 0;//TODO:add error 406)
    request_package_buffer[25] = response_data_count;
    for (uint8_t i = 0; i < request_package_buffer[25]; i++) {
      request_package_buffer[26 + i] = RS485_Serial.read();
    }
    while (RS485_Serial.available()) RS485_Serial.read();

    uint16_t CRC_calculated = calculate_CRC(true, 0, request_package_buffer[0]);
    for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
      CRC_calculated = calculate_CRC(false, CRC_calculated, request_package_buffer[i]);
    }
    uint8_t CRC_calculated_significant = CRC_calculated >> 8;
    uint8_t CRC_calculated_least = CRC_calculated % 256;

    request_package_buffer[42] = CRC_calculated_least;
    request_package_buffer[43] = CRC_calculated_significant;
    //SEND RESPONSE
    digitalWrite(EBYTE_E32_M0_PIN, LOW);
    digitalWrite(EBYTE_E32_M1_PIN, LOW);
    delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);
    //Fixed broadcast
    LoraSerial.write(request_package_buffer[4]);
    LoraSerial.write(request_package_buffer[5]);
    LoraSerial.write(DEVICE_CHANNEL);
    //Data
    for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE; i++) {
      LoraSerial.write(request_package_buffer[i]);
    }
  }
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
  while (LoraSerial.available() > 0) LoraSerial.read();

  digitalWrite(EBYTE_E32_M0_PIN, HIGH);
  digitalWrite(EBYTE_E32_M1_PIN, HIGH);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);

  for (uint8_t i = 0; i < 3; i++) LoraSerial.write(193);  //0xC1
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);
  for (uint8_t i = 0; i < 6; i++) {
    if (LoraSerial.available() == 0) break;
    ebyte_parameters[i] = LoraSerial.read();
  }

  if (print_parameters) {
    Serial.print("Current parameters of the EBYTE E32: ");
    for (uint8_t i = 0; i < 5; i++) Serial.print(String(ebyte_parameters[i]) + ", ");
    Serial.println(ebyte_parameters[5]);
  }

  digitalWrite(EBYTE_E32_M0_PIN, LOW);
  digitalWrite(EBYTE_E32_M1_PIN, LOW);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);
}

bool set_ebyte_parameters(bool print_parameters) {
  digitalWrite(EBYTE_E32_M0_PIN, HIGH);
  digitalWrite(EBYTE_E32_M1_PIN, HIGH);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);

  uint8_t parameters_to_set[6];
  parameters_to_set[0] = 192;  //0xC0
  parameters_to_set[1] = DEVICE_ADDRESS >> 8;
  parameters_to_set[2] = DEVICE_ADDRESS % 256;
  parameters_to_set[3] = (UART_PARITY_MODE & B00000011) << 6;
  parameters_to_set[3] += (UART_BAUD_MODE & B00000111) << 3;
  parameters_to_set[3] += (AIR_DATA_RATE_MODE & B00000111);
  parameters_to_set[4] = (DEVICE_CHANNEL & B00011111);
  parameters_to_set[5] = (FIXED_TRANSMISSION_MODE & B00000001) << 7;
  parameters_to_set[5] += (IO_DRIVE_MODE & B00000001) << 6;
  parameters_to_set[5] += (FEC_MODE & B00000001) << 2;
  parameters_to_set[5] += (POWER_MODE & B00000011);
  for (uint8_t i = 0; i < 6; i++) LoraSerial.write(parameters_to_set[i]);
  if (print_parameters) {
    Serial.print("Desired parameters of the EBYTE-E32: ");
    for (uint8_t i = 0; i < 5; i++) Serial.print(String(parameters_to_set[i]) + ", ");
    Serial.println(parameters_to_set[5]);
  }

  //save changes by changing operation mode
  digitalWrite(EBYTE_E32_M0_PIN, LOW);
  digitalWrite(EBYTE_E32_M1_PIN, LOW);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);
  digitalWrite(EBYTE_E32_M0_PIN, HIGH);
  digitalWrite(EBYTE_E32_M1_PIN, HIGH);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);

  LoraSerial.listen();
  while (LoraSerial.available() > 0) LoraSerial.read();

  for (uint8_t i = 0; i < 3; i++) LoraSerial.write(193);  //0xC1
  delay(100);
  for (uint8_t i = 0; i < 6; i++) {
    if (LoraSerial.available() == 0) break;
    ebyte_parameters[i] = LoraSerial.read();
  }
  if (print_parameters) {
    Serial.print("Current parameters of the EBYTE E32: ");
    for (uint8_t i = 0; i < 5; i++) Serial.print(String(ebyte_parameters[i]) + ", ");
    Serial.println(ebyte_parameters[5]);
  }

  digitalWrite(EBYTE_E32_M0_PIN, LOW);
  digitalWrite(EBYTE_E32_M1_PIN, LOW);
  delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);

  for (uint8_t i = 0; i < 6; i++) {
    if (ebyte_parameters[i] != parameters_to_set[i]) {
      if (DEBUG) Serial.println("Could not set EBYTE_E32 parameters");
      return false;
    }
  }
  if (DEBUG) Serial.println("EBYTE_E32 parameters are set");
  return true;
}

//----------------------------------------------------------------
uint16_t calculate_CRC(bool is_first_data, uint16_t previously_calculated_crc, uint16_t new_byte) {
  uint16_t key = 40961;                                          // 1010 0000 0000 0001
  if (is_first_data == true) previously_calculated_crc = 65535;  //0xFFFF

  new_byte = new_byte ^ previously_calculated_crc;

  for (int i = 0; i < 8; i++) {
    bool should_XOR = false;
    if (new_byte % 2 == 1)
      should_XOR = true;
    new_byte = new_byte >> 1;
    if (should_XOR)
      new_byte = new_byte ^ key;
  }
  return new_byte;
}

void configure_RS485_pins() {
  pinMode(RS485_SOFTWARE_SERIAL_RX_PIN, INPUT);
  pinMode(RS485_SOFTWARE_SERIAL_TX_PIN, OUTPUT);
  pinMode(RS485_OUTPUT_ENABLE_PIN, OUTPUT);
  digitalWrite(RS485_OUTPUT_ENABLE_PIN, LOW);
}
