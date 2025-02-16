#include <Stepper.h>

// Stepper Motor Setup
const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

// RGB LED Pins
const int redPin = 5;
const int greenPin = 6;
char receivedChar;  // Variable to store received character

void setup() {
    Serial.begin(9600);
    myStepper.setSpeed(15);

    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);

    // **🔴 Default state: Locked (Red ON, Green OFF)**
    digitalWrite(redPin, HIGH);  
    digitalWrite(greenPin, LOW);

    Serial.println("🔴 System Locked - Waiting for Face Recognition...");
}

void loop() {
    if (Serial.available() > 0) {
        receivedChar = Serial.read();
        
        if (receivedChar == 'U') {  // 🔓 Unlock the Door
            Serial.println("🔓 Unlocking Door");

            digitalWrite(redPin, LOW);   // 🔴 Turn OFF Red LED
            Serial.println("green Systenjfnjkfnjksnd");

            digitalWrite(greenPin, HIGH); // 🟢 Turn ON Green LED
            myStepper.step(stepsPerRevolution / 2);  // Rotate to unlock
            
            delay(5000);  // ⏳ Keep unlocked for 5 sec
            
            // **🔒 Auto-Locking After 5 Seconds**
            Serial.println("🔒 Locking Door...");
            digitalWrite(redPin, HIGH);  // 🔴 Turn ON Red LED
            digitalWrite(greenPin, LOW); // 🟢 Turn OFF Green LED
            myStepper.step(-stepsPerRevolution / 2);  // Reverse to lock
        }
    }
}