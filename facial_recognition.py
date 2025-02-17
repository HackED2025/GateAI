import cv2
import face_recognition
import pickle
import numpy as np

def facial_recognition():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    print("Loading encoded file...")
    file = open("encode_file.p", 'rb')
    encodeListToPerson = pickle.load(file)
    file.close()
    encodedPeopleList, peopleList = encodeListToPerson
    print("Encoded file loaded")

    while True:
        result, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        if not result:
            break

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodedFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodedPeopleList, encodedFace)
            faceDistance = face_recognition.face_distance(encodedPeopleList, encodedFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]: 
                print(f"Known face detected: {peopleList[matchIndex]}")
            else:
                print("No authorized face detected")

        key = cv2.waitKey(1)
        if key == 27:  # Press "Esc" to exit
            break
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

facial_recognition()