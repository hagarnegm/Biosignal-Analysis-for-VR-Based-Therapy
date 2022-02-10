#include <SoftwareSerial.h>

//Initialise Arduino to NodeMCU (5=Rx & 6=Tx)
SoftwareSerial nodemcu(5, 6);

unsigned int ch1;

void setup() {
  Serial.begin(115200);
  nodemcu.begin(115200);
  delay(1000);

  Serial.println("Program started");
}

void loop() {
  static uint32_t last_conversion_time = micros();
    if (micros() - last_conversion_time >= 1000) {
        last_conversion_time += 1000;
        ch1 = analogRead(A0);
        nodemcu.write(ch1 / 256);
        nodemcu.write(ch1 % 256);
        Serial.print(ch1);
        Serial.print(",50,300");
        Serial.println();
    }
  /*
  ch1 = analogRead(A0);
  //Send data to NodeMCU
  nodemcu.write(ch1 / 256);
  nodemcu.write(ch1 % 256);
  Serial.println(ch1);
  delay(2000);*/
}
