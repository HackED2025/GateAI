import cv2
import face_recognition
import pickle
import numpy as np
import time

# Global variables
LASTUNLOCKTIME = 0
TIMEDELAY = 300  # 5 minutes

def unlock():
    """Handles unlocking mechanism."""
    print("🔹 Sending 'U' to unlock")

def write_log(log_entry):
    """Write the log entry to a file."""
    with open("detection_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

def facial_recognition():
    global LASTUNLOCKTIME

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    try:
        print("📂 Loading encoded file...")
        try:
            with open("encode_file.p", 'rb') as file:
                encodedPeopleList, peopleList = pickle.load(file)
            print("✅ Encoded file loaded")
        except (FileNotFoundError, EOFError):
            print("❌ Error: Encoded file missing or corrupt")
            return  # Exit if the file is missing or unreadable

        while True:
            success, img = cap.read()
            if not success:
                print("❌ Error: Could not read frame")
                break  # Exit loop if camera read fails

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodedFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodedPeopleList, encodedFace)
                faceDistance = face_recognition.face_distance(encodedPeopleList, encodedFace)
                matchIndex = np.argmin(faceDistance)

                if matches[matchIndex]:  # ✅ Face Recognized
                    print(f"✅ Known face detected: {peopleList[matchIndex]}")
                    currentTime = time.time()
                    if currentTime - LASTUNLOCKTIME > TIMEDELAY:
                        unlock()  # 🔓 Unlock door
                        LASTUNLOCKTIME = currentTime  # ✅ Update unlock time
                    # Add log entry
                    log_entry = f"Face recognized: {peopleList[matchIndex]} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
                    write_log(log_entry)
                else:
                    print("❌ No authorized face detected")
                    # Add log entry for no match
                    log_entry = f"Unrecognized face detected at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
                    write_log(log_entry)

            # Encode frame to JPEG and send for streaming
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        print("🔻 Releasing camera resource...")
        cap.release()  # Ensure camera is properly closed

# Run facial recognition (this would be executed as a background process)
facial_recognition()
