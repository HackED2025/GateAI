import cv2
import face_recognition
import pickle
import os

folder = 'images'
modePathList = os.listdir(folder)
imageList = []
people = []
for path in modePathList: 
    imageList.append(cv2.imread(os.path.join(folder, path))) 
    people.append(os.path.splitext(path)[0])


def encode(imageList):
    '''
    gets the econding for every image in the list
    '''
    encodeList = []
    for image in imageList:
        # convert image from BGR to RGB
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # encode img into algorithim
        encoded_img = face_recognition.face_encodings(rgb_img)[0]
        encodeList.append(encoded_img)

    return encodeList

print('Start encoding...')
encodeList = encode(imageList)
encodeListToPerson = [encodeList, people]
print(encodeListToPerson)
print('Finished encoding')

file = open("encode_file.p", 'wb')
pickle.dump(encodeListToPerson, file)
file.close()
print('File saved')



