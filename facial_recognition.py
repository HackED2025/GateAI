import cv2
import face_recognition
import pickle
import numpy as np
import serial
import time

# track the last unlock time
LASTUNLOCKTIME = 0
TIMEDELAY = 300  # Delay in seconds (5 minutes)

# connect to Arduino via Serial (Update the port!)
arduino = serial.Serial('/dev/cu.usbmodem1201', 9600)  # Mac/Linux
# arduino = serial.Serial('COM3', 9600)  # Windows users, change COM port
time.sleep(2)  # Wait for Arduino to initialize


def unlock():
    """
    Function to handle unlocking mechanism.
    """
    print("🔹 Sending 'U' to Arduino (Unlocking)")
    arduino.write(b'U')  # 🔓 Send Unlock Signal

def facial_recognition():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    print("📂 Loading encoded file...")
    file = open("encode_file.p", 'rb')
    encodeListToPerson = pickle.load(file)
    file.close()
    encodedPeopleList, peopleList = encodeListToPerson
    print("✅ Encoded file loaded")

    while True:
        result, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        faceRecognized = False  # Default to no face recognized

        for encodedFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodedPeopleList, encodedFace)
            faceDistance = face_recognition.face_distance(encodedPeopleList, encodedFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:  # ✅ Face Recognized
                faceRecognized = True
                print(f"✅ Known face detected: {peopleList[matchIndex]}")
                global LASTUNLOCKTIME
                currentTime = time.time()
                if currentTime - LASTUNLOCKTIME > TIMEDELAY:
                        unlock()  # 🔓 Unlock door
            else:
                print("❌ No authorized face detected")

        key = cv2.waitKey(1)
        if key == 27:  # Press "Esc" to exit
            break

    cap.release()
    cv2.destroyAllWindows()

facial_recognition()