import os 
import cv2 as cv
import numpy as np


p = []
folder_path = r'C:\Users\GABRIEL\django\Facial\media\profile_image'

# Get a list of subfolders in the specified folder
subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# Get the number of subfolders
num_subfolders = len(subfolders)

# Get the names of subfolders
subfolder_names = [os.path.basename(folder) for folder in subfolders]
for i in subfolder_names:
    p.append(i)
Dir = r'C:\Users\GABRIEL\django\Facial\media\profile_image'
# haar_cascade = cv.CascadeClassifier('haar_cascade.xml')
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
features = []
labels = []
def create_train():
    for person in p:
        path = os.path.join(Dir, person)
        label = p.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
            # faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)
            faces = haar_cascade.detectMultiScale(gray)
            for (x,y,w,h) in faces:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)
create_train()
print("Training done-------------------------")
print(f' number of label is {len(labels)}')
print("-----------------------------------------------")
print(f' number of features is {len(features)}')
features = np.array(features, dtype='object')
labels = np.array(labels)
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features,labels)
face_recognizer.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)

