/*
  Optical Heart Rate Detection (PBA Algorithm) using the MAX30105 Breakout
  By: Nathan Seidle @ SparkFun Electronics
  Date: October 2nd, 2016
  https://github.com/sparkfun/MAX30105_Breakout

  This is a demo to show the reading of heart rate or beats per minute (BPM) using
  a Penpheral Beat Amplitude (PBA) algorithm.

  It is best to attach the sensor to your finger using a rubber band or other tightening
  device. Humans are generally bad at applying constant pressure to a thing. When you
  press your finger against the sensor it varies enough to cause the blood in your
  finger to flow differently which causes the sensor readings to go wonky.

  Hardware Connections (Breakoutboard to Arduino):
  -5V = 5V (3.3V is allowed)
  -GND = GND
  -SDA = A4 (or SDA)
  -SCL = A5 (or SCL)
  -INT = Not connected

  The MAX30105 Breakout can handle 5V or 3.3V I2C logic. We recommend powering the board with 5V
  but it will also run at 3.3V.
*/

#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

#define SDA_PIN 8
#define SCL_PIN 9

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;

long lastBeat = 0;
float beatsPerMinute = 0;
int beatAvg = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("ERROR,MAX30102_NOT_FOUND");
    while (1) {
      delay(1000);
    }
  }

  particleSensor.setup(
    60,    // LED brightness
    4,     // sample average
    2,     // LED mode: Red + IR
    100,   // sample rate
    411,   // pulse width
    4096   // ADC range
  );

  particleSensor.setPulseAmplitudeRed(0x24);
  particleSensor.setPulseAmplitudeIR(0x24);

  Serial.println("MOSAIC,PHYSIOLOGY,READY");
}

void loop() {

  long irValue = particleSensor.getIR();
  long redValue = particleSensor.getRed();

  // Heartbeat detection
  if (checkForBeat(irValue)) {

    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = 60.0 / (delta / 1000.0);

    if (beatsPerMinute > 20 && beatsPerMinute < 255) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;

      beatAvg = 0;

      for (byte x = 0; x < RATE_SIZE; x++) {
        beatAvg += rates[x];
      }

      beatAvg /= RATE_SIZE;
    }
  }

  // Send machine-readable data
  Serial.print("PPG,");
  Serial.print(millis());
  Serial.print(",");
  Serial.print(irValue);
  Serial.print(",");
  Serial.print(redValue);
  Serial.print(",");
  Serial.print(beatsPerMinute, 2);
  Serial.print(",");
  Serial.println(beatAvg);

  delay(20);
}