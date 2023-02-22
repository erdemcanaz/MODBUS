uint8_t package_buffer[PACKAGE_SIZE_BYTE];
bool is_valid_package = false;
uint8_t received_byte_count = 0;

void listen_and_execute_valid_computer_orders() {
  read_hardware_serial();
  validate_hardware_serial_package();
  execute_hardware_serial_package_if_valid();
}

void read_hardware_serial() {
  if (Serial.available() == 0) return;
  delay(HARDWARE_SERIAL_WAIT_COMPUTER_TRANSFER_MS);

  is_valid_package = true;
  received_byte_count = 0;

  while (Serial.available() > 0) {
    package_buffer[received_byte_count] = Serial.parseInt();
    received_byte_count += 1;
    if (Serial.peek() == '\n') break;
    if (received_byte_count >= PACKAGE_SIZE_BYTE) break;
  }
  while (Serial.available()) Serial.read();
}

void validate_hardware_serial_package() {
  if (!is_valid_package) return;

  if (received_byte_count != PACKAGE_SIZE_BYTE) {
    if (DEBUG) Serial.println("Received byte count is not enough, it is: " + String(received_byte_count));
    is_valid_package = false;
    return;
  }

  uint16_t CRC_calculated = calculate_CRC(true, 0, package_buffer[0]);
  for (uint8_t i = 1; i < PACKAGE_SIZE_BYTE - 2; i++) {
    CRC_calculated = calculate_CRC(false, CRC_calculated, package_buffer[i]);
  }
  uint8_t CRC_calculated_significant = CRC_calculated >> 8;
  uint8_t CRC_calculated_least = CRC_calculated % 256;

  uint16_t CRC_candidate_significant = package_buffer[PACKAGE_SIZE_BYTE - 1];
  uint16_t CRC_candidate_least = package_buffer[PACKAGE_SIZE_BYTE - 2];

  bool significant_does_not_match = (CRC_calculated_significant != CRC_candidate_significant);
  bool least_does_not_match = (CRC_calculated_least != CRC_candidate_least);
  if (significant_does_not_match || least_does_not_match) {
    if (DEBUG) Serial.println("Received CRC(lst-sig):" + String(CRC_candidate_least) + "," + String(CRC_candidate_significant) + ". However True CRC(lst-sig):" + String(CRC_calculated_least) + "," + String(CRC_calculated_significant));
    is_valid_package = false;
    return;
  }
}

void execute_hardware_serial_package_if_valid() {
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

  if (!is_valid_package) return;
  is_valid_package = false;
  //execute package
  if (package_buffer[2] == 99) Serial.println("Hi, I am here to redirect your package");
  if (package_buffer[2] == 1) broadcast_package_and_wait_for_reply();
}