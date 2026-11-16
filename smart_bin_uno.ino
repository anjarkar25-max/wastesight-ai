/*
 * WasteSight AI Pro — Autonomous Smart Bin Firmware (Arduino Uno)
 * Receives 1-byte UART Serial commands (9600 baud) from bridge.py:
 *   'B' -> Blue Bin (Dry Recyclable)   | Pin 2 LED + 1x Pin 13 Blink + Servo 90°
 *   'G' -> Green Bin (Wet Compost)     | Pin 3 LED + 2x Pin 13 Blink + Servo 90°
 *   'E' -> Black Bin (E-Waste)         | Pin 4 LED + 3x Pin 13 Blink + Servo 90°
 *   'R' -> Red Bin (Reject/Contam.)    | Pin 5 LED + 4x Pin 13 Blink + Servo 90°
 */

#include <Servo.h>

Servo binServo;

const int PIN_LED_BLUE   = 2;  // Dry Recyclable
const int PIN_LED_GREEN  = 3;  // Wet Compost
const int PIN_LED_EWASTE = 4;  // E-Waste
const int PIN_LED_RED    = 5;  // Reject / Contaminated
const int PIN_BOARD_LED  = 13; // Built-in Arduino Uno status LED
const int PIN_SERVO      = 9;  // SG90 Servo Motor signal pin

void setup() {
  Serial.begin(9600);

  pinMode(PIN_LED_BLUE, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_EWASTE, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_BOARD_LED, OUTPUT);

  binServo.attach(PIN_SERVO);
  binServo.write(0); // Default locked/closed lid position

  // Power-on self-test blink
  digitalWrite(PIN_BOARD_LED, HIGH);
  delay(300);
  digitalWrite(PIN_BOARD_LED, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();

    // Reset all indicator LEDs before actuating active stream
    digitalWrite(PIN_LED_BLUE, LOW);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_EWASTE, LOW);
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_BOARD_LED, LOW);

    if (cmd == 'B') { // Blue Bin - Dry Recyclable
      digitalWrite(PIN_LED_BLUE, HIGH);
      blinkBuiltin(1);
      openAndCloseLid();
    } 
    else if (cmd == 'G') { // Green Bin - Wet Compost
      digitalWrite(PIN_LED_GREEN, HIGH);
      blinkBuiltin(2);
      openAndCloseLid();
    } 
    else if (cmd == 'E') { // Black Bin - E-Waste
      digitalWrite(PIN_LED_EWASTE, HIGH);
      blinkBuiltin(3);
      openAndCloseLid();
    } 
    else if (cmd == 'R') { // Red Bin - Reject / Contaminated
      digitalWrite(PIN_LED_RED, HIGH);
      blinkBuiltin(4);
      openAndCloseLid();
    }
  }
}

void openAndCloseLid() {
  binServo.write(90);  // Rotate servo 90 degrees to open bin lid
  delay(3500);         // Hold lid open for 3.5 seconds for contactless drop
  binServo.write(0);   // Return lid to closed position
}

void blinkBuiltin(int count) {
  for (int i = 0; i < count; i++) {
    digitalWrite(PIN_BOARD_LED, HIGH);
    delay(150);
    digitalWrite(PIN_BOARD_LED, LOW);
    delay(150);
  }
}
