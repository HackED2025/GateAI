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
    #print(path)
    #print(os.path.splitext(path)[0])
    people.append(os.path.splitext(path)[0])

print(people)


def Encode(imageList):
    '''
    gets the econding for every image in the list
    '''
    for image in imageList:
        encodeList = []
        # convert image from BGR to RGB
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # encode img into algorithim
        encoded_img = face_recognition.face_encodings(rgb_img)[0]
        encodeList.append(encoded_img)

    return encodeList

print('Start encoding...')
encodeList = Encode(imageList)
encodeListToPerson = [encodeList, people]
#print(encodeList)
print('Finished encoding')

file = open("encode_file.p", 'wb')
pickle.dump(encodeListToPerson, file)
file.close()
print('File saved')



