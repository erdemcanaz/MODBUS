uint16_t holding_registers[NUMBER_OF_HOLDING_REGISTERS];
uint16_t input_registers[NUMBER_OF_INPUT_REGISTERS];

uint8_t B[32];//bytes buffer

void configure_RS485_pins() {
  pinMode(RS485_SOFTWARE_SERIAL_RX_PIN, INPUT);
  pinMode(RS485_SOFTWARE_SERIAL_TX_PIN, OUTPUT);
  pinMode(RS485_OUTPUT_ENABLE_PIN, OUTPUT);
  digitalWrite(RS485_OUTPUT_ENABLE_PIN, LOW);
}

void slave_operate() {
  if (RS485_Serial.available() >= 1)delay(WAIT_RS485_TIME_ms);
  else return; 

  uint8_t number_of_bytes_received = RS485_Serial.available();
  if(DEBUG)Serial.println("data is received: "+String(number_of_bytes_received));

  if (number_of_bytes_received == 8) {//write or read request
    for (int i = 0; i < 8; i++) {
      B[i] = RS485_Serial.read();
    }
  } else {
    while (RS485_Serial.available())RS485_Serial.read();
    return;
  }
  //---------------ERROR CHECK
  //1-ID CHECK
  if (B[0] != RS485_SLAVE_ID) {
    while (RS485_Serial.available())RS485_Serial.read();
    if(DEBUG)Serial.println("Received data is for me");
    return;//Wrong slave ID or another slave
  }
  //2-CRC CHECK
  uint16_t received_CRC = (((uint16_t)B[7]) << 8) + B[6];
  uint16_t expected_CRC = generate_CRC_16_bit(6, B[0], B[1], B[2], B[3], B[4], B[5]);

  if (received_CRC != expected_CRC) {
    while (RS485_Serial.available())RS485_Serial.read();
    if(DEBUG)Serial.println("Received data has corrupted CRC code");
    return;//CRC of the package is wrong
  }

  //------------------
  if (B[1] == 3) {//read holding registers
    if(DEBUG)Serial.println("Read holding register query");
    //QUERY: 0-ID, 1-FUNC_CODE, 2-REG_ADDR(SIG), 3-REG_ADDR(LST), 4-NUMBER_OF_REG(SIG), 5-NUMBER_OF_REG(LST), 6-CRC(LST), 7-CRC(SIG)
    uint16_t holding_register_addres = ((uint16_t)B[2] << 8) + B[3];

    if (holding_register_addres >= 0 && holding_register_addres < NUMBER_OF_HOLDING_REGISTERS) {
      if(DEBUG)Serial.println("Holding register's ("+String(holding_register_addres)+") value is:"+String(holding_registers[holding_register_addres]));
      uint8_t val_sig = holding_registers[holding_register_addres] >> 8;
      uint8_t val_lst = holding_registers[holding_register_addres] % 256;
      //RESPONSE: 0-ID, 1-FUNC_CODE, 2-BYTE_COUNT, 3-REG_VAL(SIG), 4-REG_VAL(LST), 5-CRC(LST), 6-CRC(SIG);
      slave_write(5, B[0], B[1], 2, val_sig, val_lst, 0);
    } else return;//holding register address is wrong
  }

  else if (B[1] == 4) { //read input registers
    if(DEBUG)Serial.println("Read input register query");
    //QUERY: 0-ID, 1-FUNC_CODE, 2-REG_ADDR(SIG), 3-REG_ADDR(LST), 4-NUMBER_OF_REG(SIG), 5-NUMBER_OF_REG(LST), 6-CRC(LST), 7-CRC(SIG)
    uint16_t input_register_addres = ((uint16_t)B[2] << 8) + B[3];

    if (input_register_addres >= 0 && input_register_addres < NUMBER_OF_INPUT_REGISTERS) {
      if(DEBUG)Serial.println("Input register's ("+String(input_register_addres)+") value is:"+String(input_registers[input_register_addres]));
      uint8_t val_sig = input_registers[input_register_addres] >> 8;
      uint8_t val_lst = input_registers[input_register_addres] % 256;
      //RESPONSE: 0-ID, 1-FUNC_CODE, 2-BYTE_COUNT, 3-REG_VAL(SIG), 4-REG_VAL(LST), 5-CRC(LST), 6-CRC(SIG);
      slave_write(5, B[0], B[1], 2, val_sig, val_lst, 0);
    } else return;//!input register address is wrong
  }

  else if (B[1] == 6) { //write holding registers
   if(DEBUG)Serial.println("Write holding register query");
    //QUERY: 0-ID, 1-FUNC_CODE, 2-REG_ADDR(SIG), 3-REG_ADDR(LST), 4-REG_VALUE(SIG), 5-REG_VAL(LST), 6-CRC(LST), 7-CRC(SIG)
    uint16_t holding_register_addres = ((uint16_t)B[2] << 8) + B[3];

    if (holding_register_addres >= 0 && holding_register_addres < NUMBER_OF_HOLDING_REGISTERS) {
      holding_registers[holding_register_addres] = 0;
      holding_registers[holding_register_addres] = (((uint16_t)B[4]) << 8) + B[5];
      if(DEBUG)Serial.println("Holding register's ("+String(holding_register_addres)+") new value is:"+String(holding_registers[holding_register_addres]));
      //RESPONSE: 0-ID, 1-FUNC_CODE, 2-REG_ADDR(SIG), 3-REG_ADDR(LST), 4-REG_VALUE(SIG), 5-REG_VAL(LST), 6-CRC(LST), 7-CRC(SIG)
      slave_write(6, B[0], B[1], B[2], B[3], B[4], B[5]);
    } else return;//!holding register address is wrong
  } else {
    return;//! unknown function code
  }


}

void slave_write( uint8_t number_of_bytes, uint8_t B_0, uint8_t B_1, uint8_t B_2, uint8_t B_3, uint8_t B_4, uint8_t B_5) {
  uint16_t CRC = generate_CRC_16_bit(number_of_bytes, B_0,  B_1,  B_2,  B_3,  B_4,  B_5);
  uint8_t CRC_LEAST = CRC % 256;
  uint8_t CRC_SIGNIFICANT = CRC >> 8;
  delay(WAIT_RS485_TIME_ms);

  digitalWrite(RS485_OUTPUT_ENABLE_PIN, HIGH);
  RS485_Serial.write(B_0);
  if (number_of_bytes >= 2 )  RS485_Serial.write(B_1);
  if (number_of_bytes >= 3 )  RS485_Serial.write(B_2);
  if (number_of_bytes >= 4 )  RS485_Serial.write(B_3);
  if (number_of_bytes >= 5 )  RS485_Serial.write(B_4);
  if (number_of_bytes >= 6 )  RS485_Serial.write(B_5);
  RS485_Serial.write(CRC_LEAST); //CRC (LST)
  RS485_Serial.write(CRC_SIGNIFICANT); //CRC (SIG)
  digitalWrite(RS485_OUTPUT_ENABLE_PIN, LOW);

}

//MAGICAL CRC_16 MODBUS code.
uint16_t generate_CRC_16_bit(uint8_t number_of_bytes, uint8_t B_0, uint8_t B_1, uint8_t B_2, uint8_t B_3, uint8_t B_4, uint8_t B_5) {
  uint16_t remainder = CRC_16_bit_for_1BYTE(B_0, 65535);
  if (number_of_bytes >= 2 )  remainder = CRC_16_bit_for_1BYTE(B_1, remainder);
  if (number_of_bytes >= 3 )  remainder = CRC_16_bit_for_1BYTE(B_2, remainder);
  if (number_of_bytes >= 4 )  remainder = CRC_16_bit_for_1BYTE(B_3, remainder);
  if (number_of_bytes >= 5 )  remainder = CRC_16_bit_for_1BYTE(B_4, remainder);
  if (number_of_bytes >= 6 )  remainder = CRC_16_bit_for_1BYTE(B_5, remainder);
  return remainder;

}
uint16_t CRC_16_bit_for_1BYTE(uint16_t data, uint16_t last_data) {
  //if this is first data (i.e LAST_DATA==null), LAST_DATA= 65535 = FFFF
  uint16_t key = 40961; //1010 0000 0000 0001
  data = data ^ last_data;//XOR
  for (int i = 0; i < 8; i++) {
    boolean should_XOR = false;
    if (data % 2 == 1)should_XOR = true;
    data = data >> 1;
    if (should_XOR)data = data ^ key;
  }
  return data;
}
