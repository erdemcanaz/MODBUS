uint16_t calculate_CRC(bool is_first_data, uint16_t previously_calculated_crc, uint16_t new_byte){ 
  uint16_t key = 40961; // 1010 0000 0000 0001
  if(is_first_data == true)previously_calculated_crc = 65535; //0xFFFF

  new_byte = new_byte ^ previously_calculated_crc;
  
  for (int i = 0; i < 8; i++)
  {
    bool should_XOR = false;
    if (new_byte % 2 == 1)
      should_XOR = true;
    new_byte = new_byte >> 1;
    if (should_XOR)
      new_byte = new_byte ^ key;
  }
  return new_byte;
}

