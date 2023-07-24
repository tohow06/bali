#include <SPI.h>
#include <LoRa.h>

#define ss 15
#define rst 16
#define dio0 D1
int counter = 0;


void setup() {

  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Sender");

  LoRa.setPins(ss, rst, dio0);

  while (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    delay(100);
  }
  Serial.println("LoRa Initializing OK!");
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  // send packet
  LoRa.beginPacket();
  LoRa.print(F("Pkt No:"));
  LoRa.println(counter);
  LoRa.endPacket();

  counter++;

  delay(1000);
}