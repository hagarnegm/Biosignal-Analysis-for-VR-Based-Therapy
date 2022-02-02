/*
 * This code reads analog data connected to 
 * analog pin 0, and transmits it via serial
 * port. It uses a strategy similar to blink 
 * without delay to achieve a data rate of 
 * about 1000 samples per second. 
 */

 // TODO: Consider using a timer instead.
 
int analog0;
void setup() {
  Serial.begin(115200);
}

void loop() {
    static uint32_t last_conversion_time = micros();
    if (micros() - last_conversion_time >= 1000) {
        last_conversion_time += 1000;
        analog0 = analogRead(A0);
        Serial.println(analog0);
    }
}
