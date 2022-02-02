/* 
 *  This code reads serial data from arduino,
 *  and transmits it over wifi. It assumes that 
 *  The arduino analog pins 5, 6 are connected to
 *  node mcu pins D5 and D6. It has been tested
 *  with baudrate of 9600 and with delay of 2ms.
 *  To send data at higher rates, adjust the boad
 *  rate and delay accordingly.
 */

#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>

int port = 8888;  //Port number
WiFiServer server(port);

//Edit this to add your network ssid and password
const char *ssid = "";
const char *password = "";

SoftwareSerial nodemcu(D6, D5);

void setup() 
{
  Serial.begin(115200);
  nodemcu.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); //Connect to wifi
 
  // Wait for connection  
  Serial.println("Connecting to Wifi");
  while (WiFi.status() != WL_CONNECTED) {   
    delay(500);
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  
  server.begin();
  Serial.print("Open Telnet and connect to IP:");
  Serial.print(WiFi.localIP());
  Serial.print(" on port ");
  Serial.println(port);
}

void loop() 
{
  WiFiClient client = server.available();
  
  if (client) {
    if(client.connected())
    {
      Serial.println("Client Connected");
    }
    
    while(client.connected()){   
      unsigned int val;
  
      while(!nodemcu.available()) {}
      byte b1 = nodemcu.read();
      
      while(!nodemcu.available()) {}
      byte b2 = nodemcu.read();

      val = b1*256 + b2;
      
      client.write("Recieved Pot:  ");
      client.println(val);
      
    }
    client.stop();
    Serial.println("Client disconnected");    
  }
}
