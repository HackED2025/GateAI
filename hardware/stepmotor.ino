#include <Stepper.h>

// 🔹 Define constants
const int stepsPerRevolution = 2048;  // Steps per full revolution
const int motorSpeed = 15;  // Speed in RPM
const int runTime = 10000;  // 🔹 5 seconds in milliseconds
bool motorShouldMove = true;  // Start moving

// 🔹 Initialize stepper motor on pins 8, 10, 9, 11
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  myStepper.setSpeed(motorSpeed);
  Serial.begin(9600);
  Serial.println("🔹 Motor will run for 5 seconds...");
  
  unsigned long startTime = millis();  // 🔹 Record start time

  while (millis() - startTime < runTime) {  // 🔹 Run for 5 seconds
    myStepper.step(stepsPerRevolution / 10);  // 🔹 Smooth movement
  }

  Serial.println("🔹 Motor stopped.");
}

void loop() {
  // 🔹 Empty because motor runs in setup() for 5 sec and stops
}