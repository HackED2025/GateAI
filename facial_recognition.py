import cv2
import face_recognition
import pickle
import numpy as np
import tensorflow as tf
import serial
import time
import json

LASTUNLOCKTIME = 0
TIMEDELAY = 300  # Delay in seconds (5 minutes)

def unlock():
    print("🔹 Sending 'U' to Arduino (Unlocking)")
    arduino.write(b'U')  # 🔓 Send Unlock Signal

def facial_recognition():
    print("begin")

    with open('my_model.json', 'r') as f:
        gesture_model_json = f.read()
        gesture_model = tf.keras.models.model_from_json(gesture_model_json)
        gesture_model.load_weights('gesture_model.h5')

    with open('meta_model.json', 'r') as f:
        meta_model_json = f.read()
        meta_model = tf.keras.models.model_from_json(meta_model_json)
        meta_model.load_weights('meta_model.h5')

    print("model loaded")

    cap = cv2.VideoCapture(0)  # Ensure camera is opened
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open camera.")
    cap.set(3, 1280)
    cap.set(4, 720)

    print("Loading encoded file...")
    with open("encode_file.p", 'rb') as file:
        encodedPeopleList, peopleList = pickle.load(file)
    print("Encoded file loaded")

    while True:
        result, img = cap.read()
        if not result:
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        detected_faces = []
        for encodedFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodedPeopleList, encodedFace)
            faceDistance = face_recognition.face_distance(encodedPeopleList, encodedFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                detected_faces.append(peopleList[matchIndex])
                print(f"Known face detected: {peopleList[matchIndex]}")
                global LASTUNLOCKTIME
                currentTime = time.time()
                if currentTime - LASTUNLOCKTIME > TIMEDELAY:
                    unlock()
            else:
                print("No authorized face detected")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (14739,))
        gesture_prediction = gesture_model.predict(np.expand_dims(resized, axis=0))
        gesture_label = np.argmax(gesture_prediction)
        print(f"🖐 Gesture detected: {gesture_label}")

        metadata = f"Faces: {', '.join(detected_faces)} | Gesture: {gesture_label}"

        ret, buffer = cv2.imencode('.jpg', img)
        if not ret:
            continue
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
