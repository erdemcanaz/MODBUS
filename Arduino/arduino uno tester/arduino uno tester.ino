//For Arduino Uno
#define DIGITAL_PIN_COUNT 12
int digital_pins[] = { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 };
#define ANALOG_PIN_COUNT 6
int analog_pins[] = { 14, 15, 16, 17, 18, 19 };

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("All pins are set to INPUT");
  Serial.println("Choose which process to execute");
  Serial.println("a. Blink all pins for ten seconds");
  Serial.println("b. Read all pins for ten seconds");

  while(true){
    char c=0;
    if(Serial.available() > 0){
      c = Serial.read();
      if(c == 'a'){
        Serial.println("Blinking all pins for ten seconds");
        blink_all_pins_ten_sec();
        break;
      }else if(c == 'b'){
        Serial.println("Reading all pins for ten seconds");
        read_all_pins_for_ten_sec();
        break;
      }
    }
  
  
  }
}


void blink_all_pins_ten_sec() {
  for (int i = 0; i < DIGITAL_PIN_COUNT; i++) {
    pinMode(digital_pins[i], OUTPUT);
  }
  for (int i = 0; i < ANALOG_PIN_COUNT; i++) {
    pinMode(analog_pins[i], OUTPUT);
  }

  for (int counter = 0; counter < 10; counter += 1) {

    // Pins are high for 500ms
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++) {
      digitalWrite(digital_pins[i], HIGH);
    }
    for (int i = 0; i < ANALOG_PIN_COUNT; i++) {
      digitalWrite(analog_pins[i], HIGH);
    }
    delay(500);

    //Pins are low for 500ms
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++) {
      digitalWrite(digital_pins[i], LOW);
    }
    for (int i = 0; i < ANALOG_PIN_COUNT; i++) {
      digitalWrite(analog_pins[i], LOW);
    }
    delay(500);

  }
}

void read_all_pins_for_ten_sec(){
  for (int i = 0; i < DIGITAL_PIN_COUNT; i++) {
    pinMode(digital_pins[i], INPUT);
  }
  for (int i = 0; i < ANALOG_PIN_COUNT; i++) {
    pinMode(analog_pins[i], INPUT);
  }

  for (int counter = 0; counter < 10; counter += 1) {
    for (int i = 0; i < DIGITAL_PIN_COUNT; i++) {
      int digital_pin_value = digitalRead(digital_pins[i]);
      Serial.print("Pin ");
      Serial.print(digital_pins[i]);
      Serial.print(":");
      Serial.println(digital_pin_value);
    }
    for (int i = 0; i < ANALOG_PIN_COUNT; i++) {
      int analog_pin_value = analogRead(analog_pins[i]);
      Serial.print("Pin A");
      Serial.print(i);
      Serial.print(":");
      Serial.println(analog_pin_value);
    }
    Serial.println();
    delay(2000);
  }

}
