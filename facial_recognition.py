import cv2
import face_recognition
import pickle
import numpy as np

def facial_recognition():
        # load camera (0 is the first camera)
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        # load encoding file
        print("loading encoded file...")
        file = open("encode_file.p", 'rb')
        encodeListToPerson = pickle.load(file)
        #print(encodeListToPerson)
        file.close()
        encodedPeopleList, peopleList = encodeListToPerson 
        #print(peopleList)
        print("Encoded file loaded")


        while True: 
                result, img = cap.read()

                # scale down image
                imgS = cv2.resize(img,(0,0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                # find location of the face and encode it
                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

                for encodedFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
                        matches = face_recognition.compare_faces(encodedPeopleList, encodedFace)
                        faceDistance = face_recognition.face_distance(encodedPeopleList, encodedFace)
                        #print("matches", matches)
                        #print("face Distance", faceDistance)

                        matchIndex = np.argmin(faceDistance)
                        #print("match index", matchIndex)

                        faceRecognized = False
                        if matches[matchIndex]:
                                faceRecognized = True
                                print("known face detected:", peopleList[matchIndex])
                                #once its true you should send a message to open the lock or return true??
                        else:
                                print("no face detected")
                

                #cv2.imshow("webcam", img)

                key = cv2.waitKey(1)
                if key == 27: #s key
                        break
                
        cap.release()
        cv2.destroyAllWindows()

        return faceRecognized

facial_recognition()