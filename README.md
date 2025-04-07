# GateAI Real-Time Threat Detection System
# Project Overview
GateAI addresses the critical need for proactive threat detection in public spaces, particularly in schools. Utilizing advanced facial and gesture recognition, GateAI offers an innovative solution to identify suspicious behavior and prevent incidents before they occur. The system integrates seamlessly with Arduino hardware for access control and a responsive web interface for real-time monitoring and alerts.

Check out the full demo here: [GateAI Project Demo](https://youtu.be/O91VX3s7MjM).

# Features
## 1. Threat Detection
- Identifies suspicious facial expressions and gestures using AI-powered recognition.

## 2. Real-Time Processing
- Analyzes live video feed to detect potential threats instantly.

## 3. Hardware Integration
- Interfaces with Arduino for automated door control and security response.

## 4. Web Interface
- Provides real-time threat monitoring and alerts through a responsive web-based dashboard.

## 5. Database Management
- Stores security events securely with SQLAlchemy for future analysis and auditing.
# How It Works
## Step 1: Data Collection
- Captures live video feed from connected cameras to monitor facial expressions and gestures.
## Step 2: Signal Processing
- Processes video frames in real-time to detect faces and recognize gestures.
- Identifies individuals using facial recognition.
- Classifies gestures using a trained AI model.
## Step 3: Threat Analysis and Response
- Uses AI to analyze detected faces and gestures to assess potential threats.
- Provides immediate alerts to security personnel through the web interface.
# Future Enhancements
- Enhanced AI Models – Improve accuracy for better threat detection.
- Additional Hardware Support – Integrate more sensors and devices.
- Database for Known People – Implement a database to store and manage known individuals.
- Notification Alerts – Add a system to send alerts for suspicious activities to security personnel.
# Acknowledgements
- Libraries – TensorFlow, OpenCV, SQLAlchemy, Arduino.
- Teachable Machine – Used (https://teachablemachine.withgoogle.com/train/pose) for gesture recognition.
- Arduino Community – For open-source hardware support.
- HackED 2025 Organizers – For fostering innovation and collaboration during the event.
- Team Members – For their dedication, creativity, and teamwork in bringing GateAI to life.
# License
This project is licensed under the MIT License.

