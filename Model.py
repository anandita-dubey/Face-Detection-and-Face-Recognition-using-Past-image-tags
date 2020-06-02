import face_recognition
from PIL import Image, ImageDraw
import PIL
import numpy as np
import sys
import os
import time

def predict(imageFile):
    uploaded_image = face_recognition.load_image_file(imageFile)
    uploaded_image_faces=face_recognition.face_locations(uploaded_image)
    print('\nCordinates for detected faces:',uploaded_image_faces)
    uploaded_image_encoding = face_recognition.face_encodings(uploaded_image,known_face_locations=uploaded_image_faces)
    encoded_face=[]
    faces_dict={}
    face_list=[]
    i=0
    for face in uploaded_image_encoding:
        if len(os.listdir('./static/uploads'))>1:
            for class_dir in os.listdir('./static/uploads'):
                if "imageEncodedData.txt" in os.listdir(os.path.join('./static/uploads',class_dir)):
                    with open(os.path.join("./static/uploads",class_dir)+"/"+"imageEncodedData.txt", "r") as filehandle:
                        filecontents = filehandle.readlines()
                        for line in filecontents:
                            current_place = line[:-1]
                            encoded_face.append(float(current_place))
                        if len(encoded_face)==128:
                            compare_face=face_recognition.compare_faces([encoded_face],face,tolerance=0.55)
                        if compare_face[0]==True:
                            faces_dict['name']=class_dir
                            faces_dict['left']=uploaded_image_faces[i][3]
                            faces_dict['top']=uploaded_image_faces[i][0]
                            faces_dict['width']=uploaded_image_faces[i][1]-uploaded_image_faces[i][3]
                            faces_dict['height']=uploaded_image_faces[i][2]-uploaded_image_faces[i][0]
                            face_distance=face_recognition.face_distance([encoded_face],face)
                            print(i,'.',faces_dict,'Face Encoding Difference:',face_distance,'\n')
                            dictionary_copy=faces_dict.copy()
                            face_list.append(dictionary_copy)
                            encoded_face=[]
                            break
                        else:
                            encoded_face=[]
                # else:
               #     encoded_face=[]
            else:
                faces_dict['name']='Unknown'
                faces_dict['left']=uploaded_image_faces[i][3]
                faces_dict['top']=uploaded_image_faces[i][0]
                faces_dict['width']=uploaded_image_faces[i][1]-uploaded_image_faces[i][3]
                faces_dict['height']=uploaded_image_faces[i][2]-uploaded_image_faces[i][0]
                print(i,'.',faces_dict,'\n')
                dictionary_copy=faces_dict.copy()
                face_list.append(dictionary_copy)
        else:
            faces_dict['name']='Unknown'
            faces_dict['left']=uploaded_image_faces[i][3]
            faces_dict['top']=uploaded_image_faces[i][0]
            faces_dict['width']=uploaded_image_faces[i][1]-uploaded_image_faces[i][3]
            faces_dict['height']=uploaded_image_faces[i][2]-uploaded_image_faces[i][0]
            print(i,'.',faces_dict,'\n')
            dictionary_copy=faces_dict.copy()
            face_list.append(dictionary_copy)
        i+=1
    print('Predicted Face List:',face_list,'\n')
    return face_list
# predict('S:/Flask course/testImages/http___com.ft.imagepublish.upp-prod-us.s3.amazonaws.jpg')

def encode_face(path):
    if "imageEncodedData.txt" not in os.listdir(path):
        imageFile=os.listdir(path)
        uploaded_image = face_recognition.load_image_file(path+'/'+imageFile[0])
        uploaded_image_faces=face_recognition.face_locations(uploaded_image)
        uploaded_image_encoding = face_recognition.face_encodings(uploaded_image,known_face_locations=uploaded_image_faces)
        with open(path+'/'+'imageEncodedData.txt', 'w') as filehandle:
                for listitem in uploaded_image_encoding:
                    for i in list(listitem):
                        filehandle.write('%s\n' % i)
        print("Successfully Encoded Face")
