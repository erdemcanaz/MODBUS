//Functions for device_1_master_script
uint8_t package_buffer[PACKAGE_SIZE_BYTE];

void listen_and_execute_computer_orders() {
  if (Serial.available() == 0) return;

  //(1)______________________________________________________________________________________________________________
  delay(HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS);
  uint8_t received_byte_count = 0;
  while (Serial.available() > 0) {
    package_buffer[received_byte_count] = Serial.parseInt();
    received_byte_count += 1;
    if (Serial.peek() == '\n' || received_byte_count >= PACKAGE_SIZE_BYTE) break;
  }
  while (Serial.available()) Serial.read();


  //(2)______________________________________________________________________________________________________________
  bool is_received_byte_count_correct = (received_byte_count == PACKAGE_SIZE_BYTE);
  bool is_received_CRC_correct = true;

  uint16_t CRC_calculated = calculate_CRC(true, 0, package_buffer[0]);
  for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
    CRC_calculated = calculate_CRC(false, CRC_calculated, package_buffer[i]);
  }
  is_received_CRC_correct = ((CRC_calculated >> 8) == package_buffer[PACKAGE_SIZE_BYTE - 1]) && ((CRC_calculated % 256) == package_buffer[PACKAGE_SIZE_BYTE - 2]);

  if (!is_received_byte_count_correct || !is_received_CRC_correct) {
    if (DEBUG && !is_received_byte_count_correct) Serial.println("Received byte count is not enough, it is: " + String(received_byte_count));
    else if (DEBUG && !is_received_CRC_correct) Serial.println("Received CRC(lst-sig):" + String(package_buffer[PACKAGE_SIZE_BYTE - 2]) + "," + String(package_buffer[PACKAGE_SIZE_BYTE - 1]) + ". However True CRC(lst-sig):" + String((CRC_calculated % 256)) + "," + String((CRC_calculated >> 8)));
    return_error_package(43);  //Computer data package is corrupted
    return;
  }

  //(3)______________________________________________________________________________________________________________

  //(3.0)_________________
  if (package_buffer[3] == 1 && package_buffer[4] == 99) {
    package_buffer[26] = 1;
    package_buffer[27] = DEVICE_ADDRESS;
    return_error_package(1);  //Greet computer  
    return;
  }

  //(3.1)_________________
  else if (package_buffer[3] == 2 && package_buffer[4] == 0) {
    uint8_t reply_package_buffer[PACKAGE_SIZE_BYTE];

    //(3.1.0-SEND REQUEST)
    if (digitalRead(EBYTE_E32_M0_PIN) || digitalRead(EBYTE_E32_M1_PIN)) {
      digitalWrite(EBYTE_E32_M0_PIN, LOW);
      digitalWrite(EBYTE_E32_M1_PIN, LOW);
      delay(EBYTE_OPERATION_MODE_CHANGE_DELAY_MS);
    }
    package_buffer[5] = DEVICE_ADDRESS >> 8;   //Master lora address significant
    package_buffer[6] = DEVICE_ADDRESS % 256;  //Master lora address least

    uint16_t CRC_calculated = calculate_CRC(true, 0, package_buffer[0]);
    for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
      CRC_calculated = calculate_CRC(false, CRC_calculated, package_buffer[i]);
    }
    package_buffer[PACKAGE_SIZE_BYTE - 2] = CRC_calculated % 256;
    package_buffer[PACKAGE_SIZE_BYTE - 1] = CRC_calculated >> 8;

    //(3.1.0.0-fixed broadcast)
    LoraSerial.write(package_buffer[7]);
    LoraSerial.write(package_buffer[8]);
    LoraSerial.write(DEVICE_CHANNEL);
    //(3.1.0.1-package broadcast)
    for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE; i++) {
      LoraSerial.write(package_buffer[i]);
    }

    //(3.1.1-GET RESPONSE)
    if (!LoraSerial.isListening()) LoraSerial.listen();
    while (LoraSerial.available()) LoraSerial.read();
    delay(LORA_REQUEST_WAIT_REPLY_TIME_MS);

    if (LoraSerial.available() == 0) {
      if (DEBUG) Serial.println("No reply is received for process(" + String(package_buffer[1])+ "-" + String(package_buffer[2]) + ")");
      while (LoraSerial.available()) LoraSerial.read();
      return_error_package(89);  //No reply is received for process
      return;
    } else if (LoraSerial.available() != PACKAGE_SIZE_BYTE) {
      if (DEBUG) Serial.println("Number of bytes received as reply do not match with package format -> received bytes:" + String(LoraSerial.available()) + "");
      while (LoraSerial.available()) LoraSerial.read();
      return_error_package(243);  //Number of bytes received as reply do not match with package format
      return;
    }

    for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE; i++) {
      reply_package_buffer[i] = LoraSerial.read();
    }

    if (DEBUG) Serial.println("Reply is received for process(" + String(package_buffer[1])+ "-" + String(package_buffer[2]) + ")");
    for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE - 1; i++) {
      Serial.print(String(reply_package_buffer[i]) + ",");
    }
    Serial.println(reply_package_buffer[PACKAGE_SIZE_BYTE - 1]);
    while (LoraSerial.available()) LoraSerial.read();
  }

  //(3.x)_________________
  else{
    return_error_package(0); //Function code and Subfunction code does not match with any of the master node methods
    return;
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

void return_error_package(uint8_t status_code) {
  package_buffer[0] = status_code;
  uint16_t CRC_calculated = calculate_CRC(true, 0, package_buffer[0]);
  for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) CRC_calculated = calculate_CRC(false, CRC_calculated, package_buffer[i]);
  package_buffer[PACKAGE_SIZE_BYTE - 2] = CRC_calculated % 256;
  package_buffer[PACKAGE_SIZE_BYTE - 1] = CRC_calculated >> 8;

  for (uint8_t i = 0; i < PACKAGE_SIZE_BYTE - 1; i++) {
    Serial.print(String(package_buffer[i]) + ",");
  }
  Serial.println(package_buffer[PACKAGE_SIZE_BYTE-1]);
}
