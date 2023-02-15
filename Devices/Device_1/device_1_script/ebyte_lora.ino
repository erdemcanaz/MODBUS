
void configure_ebyte_pins(){
  pinMode(EBYTE_TX_PIN, INPUT);
  pinMode(EBYTE_RX_PIN, OUTPUT);
  pinMode(EBYTE_M0_PIN, OUTPUT);
  pinMode(EBYTE_M1_PIN, OUTPUT);
  pinMode(EBYTE_AUX_PIN, INPUT);
}

uint8_t ebyte_parameters[6];
void get_ebyte_parameters(bool print_parameters){
  while(digitalRead(EBYTE_AUX_PIN)==0)continue;

  lora_serial_instance.listen();
  while(lora_serial_instance.available()>0)lora_serial_instance.read();

  digitalWrite(EBYTE_M0_PIN, HIGH);
  digitalWrite(EBYTE_M1_PIN,HIGH);
  for(uint8_t i=0;i<3;i++)lora_serial_instance.write(193);//0xC0
  delay(EBYTE_DELAY_MS);

  for(uint8_t i = 0;i<6;i++){
    if(lora_serial_instance.available()==0)break;
    ebyte_parameters[i] = lora_serial_instance.read();
  }

  if(print_parameters){
    Serial.println("--------------------");
    for(uint8_t i=0;i<6;i++)Serial.print(String(ebyte_parameters[i])+", ");
    Serial.println();
    Serial.println("DEVICE-CHANNEL         :"+String( ((ebyte_parameters[4])&B00011111)));
    Serial.println("DEVICE-ADDRESS         :"+String(uint16_t(ebyte_parameters[1])*256+ebyte_parameters[2] ));
    Serial.println("UART-PARITY-MODE       :"+String((ebyte_parameters[3]&B11000000)>>6));
    Serial.println("UART-BAUD-MODE         :"+String((ebyte_parameters[3]&B00111000)>>3));
    Serial.println("AIR-DATA-RATE-MODE     :"+String((ebyte_parameters[3]&B00000111)));
    Serial.println("FIXED-TRANSMISSION-MODE:"+String((ebyte_parameters[5]&B10000000)>>7));
    Serial.println("IO-DRIVE-MODE          :"+String((ebyte_parameters[5]&B01000000)>>6));
    Serial.println("WIRELESS-WAKE-UP-MODE  :"+String((ebyte_parameters[5]&B00111000)>>3));
    Serial.println("FEC-MODE               :"+String((ebyte_parameters[5]&B00000100)>>2));
    Serial.println("POWER-MODE             :"+String((ebyte_parameters[5]&B00000011)));
    Serial.println("--------------------");

  } 

  

}


