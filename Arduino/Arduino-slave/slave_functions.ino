uint8_t reg_software_serial[SOFTWARE_SERIAL_CHAR_REGISTER_SIZE];
uint8_t s_serial_chars_to_write = 0;
uint8_t s_serial_chars_read  = 0;

uint8_t reg_hardware_serial[HARDWARE_SERIAL_CHAR_REGISTER_SIZE];

void s_serial_append_new_char_to_write(uint8_t c){
  s_serial_chars_read=0;
  if(s_serial_chars_to_write>=64)s_serial_chars_to_write=63;
  
  reg_software_serial[s_serial_chars_to_write]= c;
  s_serial_chars_to_write+=1;

}
void software_serial_write_chars(){
  for(uint8_t i = 0; i< s_serial_chars_to_write; i++){
    s_serial_instance.write(reg_software_serial[i]);
  }
  s_serial_chars_to_write = 0;
}
void software_serial_read_chars(){
  s_serial_chars_to_write = 0;

  if(s_serial_instance.available()){
    delay(10);
    while(s_serial_instance.available()>0){

      if(s_serial_chars_read>=64)s_serial_chars_read = 63;
      
      char c = s_serial_instance.read();
      reg_software_serial[s_serial_chars_read] = c;
      s_serial_chars_read+=1;

    }
   

  }
}