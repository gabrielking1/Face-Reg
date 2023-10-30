from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth
import os 
import cv2 as cv
import numpy as np
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate
from .forms import RegForm, UserProfileForm, RegistrationForm, CourseForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm 
# Create your views here.
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from .models import  UserProfile, Course , Registration
from urllib.request import urlopen
import cv2 as cv
import numpy as np
from django.http import HttpResponse
from Myapp.face_train import face_recognizer
import os
from django.conf import settings




def index(request):
    return render(request, 'home.html')


def register(request):
 
    if request.user.is_authenticated and request.user.is_superuser is False:
        return redirect('index')
     
    if request.method == 'POST':
        form = RegForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            auth.login(request, user)
            return redirect('index')
         
        else:
            messages.error(request,'you are registered already')
            return render(request,'reg.html',{'form':form})
     
    else:
        form = RegForm()
        return render(request,'reg.html',{'form':form})

def course(request):
 
    if request.user.is_authenticated:
        userr = User.objects.get(id=request.user.id)
        course = Registration.objects.all()
        courses = Registration.objects.filter(username_id = request.user.id)
        if request.method == 'POST':
            
            form = CourseForm(request.POST)
    
            if form.is_valid():
                form.save()
                return redirect('index')
                # username = form.cleaned_data['username']
                # password = form.cleaned_data['password1']
                # user = authenticate(username = username,password = password)
                # auth.login(request, user)
                # return redirect('index')
            
            else:
                form = CourseForm(initial = {'username':request.user})
                print('something is wromg')
                return render(request,'course.html',{'form':form,'course':course,'courses':courses})
        
        else:
            form = CourseForm(initial = {'username':request.user})
            return render(request,'course.html',{'form':form,'course':course,'courses':courses})
    else:
        messages.error(request, 'you are not logged in')
        return redirect('login')
    
    
def edit(request, id):
    if request.user.is_active and request.user.is_authenticated:
        
        course= get_object_or_404(Registration, id=id)
        if course.username == request.user:
            if request.method == "POST":
                form = CourseForm(request.POST, instance=course)
                if form.is_valid():
                    # username = form.cleaned_data['username']
                    password = form.cleaned_data['course']
                    # print(f' this is username {username} with {password}')
                    messages.success(request,f'course updated succesfully')
                    form.save()
                    return HttpResponseRedirect(reverse("edit", args={course.id}))
                    
                    # user = authenticate(username = username,password = password)
                    # auth.login(request, user)
                    # return redirect('index')
                
                else:
                    form = CourseForm(instance=course,initial = {'username':request.user})
                    print('something is wromg')
                    return render(request,'edit.html',{'form':form,'course':course})
            
            else:
                form = CourseForm(instance=course,initial = {'username':request.user})
                return render(request,'edit.html',{'form':form,'course':course})
        else:
            messages.error(request, 'you are not Authorized in')
        return redirect('login')
    else:
        messages.error(request, 'you are not logged in')
        return redirect('login')

def login(request):

    if request.user.is_authenticated:
        messages.info(request, 'you are logged in already')
        return redirect('index')
     
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'user not authorized')
            return redirect('login')
     
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    

def logout(request):
    auth.logout(request)
    return redirect('login')


def face_reg(request):

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
 
        if form.is_valid():
            form.save()
            return redirect('index')
         
        else:
            return render(request,'register.html',{'form':form})
     
    else:
        form = UserProfileForm({'face_id':request.user.id,})
        return render(request,'reg.html',{'form':form})



def save_image_to_user_folder(username, image_file):
    # Get the path to the user's folder
    user_folder = os.path.join(settings.MEDIA_ROOT,'profile_image', username)

    # If the user's folder does not exist, create it
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Get the file name and path for the image
    filename = image_file.name
    file_path = os.path.join(user_folder, filename)

    # Save the image to the user's folder
    with open(file_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    # Return the file path for the saved image
    return file_path


def image_upload(request):
    context = dict()
    # path = r'C:\Users\GABRIEL\django\Facial\media\test_img'
    if request.method == 'POST':
        username = request.POST.get('username')
        userr = User.objects.get(id=username)
        # print(username.username)
        address =  request.POST.get('address')
        phone =  request.POST.get('phone')
        image_path = request.POST.get('image')  # src is the name of input attribute in your html file, this src value is set in javascript code
        image = NamedTemporaryFile()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        if image is not None:
            if UserProfile.objects.filter(face_id=userr).exists():
                messages.error(request, 'you are have data with us already')
                return redirect('upload')
            else:
                obj = UserProfile.objects.create(face_id=userr, image=image, address =address, phone = phone)
                file_path = save_image_to_user_folder(userr.username, image)  # create a object of Image type defined in your model
                obj.save()
                context["path"] = obj.image.url  #url to image stored in my server/local device
            # context["username"] = obj.username
                return redirect('/')
        else :
            return redirect('/')
        return redirect('upload')
    return render(request, 'indexx.html', context=context)


def recognize_face(request):
    # try:

        if request.user.is_superuser:
            face_recognizer = cv.face.LBPHFaceRecognizer_create()
            face_recognizer.read('face_trained.yml')
            search = request.GET.get('search')
            if search:
                courses = Course.objects.filter(course_code__icontains = search).exists()
                if courses:

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

                    # Capture an image from the webcam
                    cap = cv.VideoCapture(0)
                    ret, frame = cap.read()
                    cap.release()
                    
                    
                    # Convert the image to grayscale
                    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    
                    # Detect faces in the image
                    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
                            
                    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)
                    faces = face_cascade.detectMultiScale(gray)
                    
                    # If a single face is detected, recognize it as a student face
                    if len(faces) == 1:
                        x, y, w, h = faces[0]
                        face = gray[y:y+h, x:x+w]
                        label, confidence = face_recognizer.predict(face)
                        # student = UserProfile.objects.get(face_id=label)
                        if confidence <=60:
                            print("this is confidence ",confidence)
                            student = User.objects.get(username__icontains = p[label])
                            courser = Course.objects.get(course_code__icontains = search)
                            # print("this is course ",course.course_title)
                            confirm = Registration.objects.filter(course=courser, username=student).exists()
                            print(" this is regis ", confirm)

                            if confirm :
                                print(" this student exist",)
                            # return HttpResponse(f'Student  {p[label]} recognized successfully.')
                                messages.success(request, f'Student  {p[label]} recognized and registers {search}.')
                                return redirect('recognize')
                            else:
                                messages.success(request, f'Student {p[label]}  doesnt register for this course.')
                                return redirect('recognize')
                 
                        else:
                            print("this is confidence ",confidence)
                            # return HttpResponse('Error: Could not recognize student.')
                            messages.success(request, f'Error: Could not recognize this person as a student..')
                            return redirect('recognize')
                    else:
                        messages.success(request, f'Error: Could not detect a single face.')
                        return render(request,template_name="rec.html")
                else:
                    messages.error(request, f'invalid course title')
                    return redirect('recognize')
            else:
                # messages.success(request, f'Error: Could not detect a single face.')
            # return HttpResponse('Error: Could not detect a single face.')
                return render(request,template_name="rec.html")
        else:
            messages.error(request, 'you are not authorized to this page')
            return redirect('login')  
    # except:
    #     return render(request,template_name="error.html")



# def recognize_face(request):
#     vid = cv.VideoCapture(0)

#     while(True):
        
#         # Capture the video frame
#         # by frame
#         ret, frame = vid.read()

#         # Display the resulting frame
#         # cv.imshow('frame', frame)
#          # Convert the image to grayscale
#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
#         # Detect faces in the image
#         face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)


#         if len(faces) == 1:
#             x, y, w, h = faces[0]
#             face = gray[y:y+h, x:x+w]
            
#             label, confidence = face_recognizer.predict(face)
           
#             student = UserProfile.objects.get(face_id=request.user.id)
#             if confidence < 50:
#                 return HttpResponse(f'Student recognized successfully.')
#             else:
#                 return HttpResponse('Error: Could not recognize student.')


#         # the 'q' button is set as the
#         # quitting button you may use any
#         # desired button of your choice
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     # After the loop release the cap object
#     # vid.release()
#     # Destroy all the windows
#     cv.destroyAllWindows()
#     # face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     # img = cv.imread('Gee.png')
#     cv.imshow('image',face )

    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)
    # if len(faces) == 1:
    #     x, y, w, h = faces[0]
    #     face = gray[y:y+h, x:x+w]
        
    #     label, confidence = face_recognizer.predict(face)
        
    #     student = UserProfile.objects.filter(image=face)
    #     if confidence > 50:
    #         return HttpResponse(f'Student {student.face_id.username} recognized successfully.')
    #     else:
    #         return HttpResponse('Error: Could not recognize student.')
    # else:
    #     return HttpResponse('Error: Could not detect a single face.')
    # # return render(request,template_name="rec.html")

    # video_capture = cv.VideoCapture(0)
    # while True:
    #     # Capture frame-by-frame
    #     ret, frame = video_capture.read()    
    #     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  
    # face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')  
    #     faces = face_cascade.detectMultiScale(
    #         gray,
    #         scaleFactor=1.1,
    #         minNeighbors=5,
    #         minSize=(30, 30),
    #         flags=cv.CASCADE_SCALE_IMAGE
    #     )    # Draw a rectangle around the faces
    #     for (x, y, w, h) in faces:
    #         cv.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)    # Display the resulting frame
    #         faces = gray[y:y + h, x:x + w]
            
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break# When everything is done, release the capture
    # video_capture.release()
    # img = cv.imread('Gee.jpg')

    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)
    # if len(faces) == 1:
    #     x, y, w, h = faces[0]
    #     face = gray[y:y+h, x:x+w]
        
    #     label, confidence = face_recognizer.predict(face)
        
    #     student = UserProfile.objects.filter(image=face)
    #     if confidence < 50:
    #         return HttpResponse(f'Student {student.face_id.username} recognized successfully.')
    #     else:
    #         return HttpResponse('Error: Could not recognize student.')
    
    # return render(request,template_name="rec.html")









































# def recognize_face(request):
#     faceCascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     video_capture = cv.VideoCapture(0)
#     while True:
#         # Capture frame-by-frame
#         ret, frame = video_capture.read()    
#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
#         faces = faceCascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30),
#             flags=cv.CASCADE_SCALE_IMAGE
#         )    # Draw a rectangle around the faces
#         for (x, y, w, h) in faces:
#             cv.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)    # Display the resulting frame
#             faces = gray[y:y + h, x:x + w]
#             cv.imshow('Video',faces) 
#             cv.imwrite("Gee.png", faces)   
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break# When everything is done, release the capture
#     video_capture.release()
#     cv.destroyAllWindows()
#     image = cv.imread('Gee.png')
#     cv.imshow('saved faces', image)
#     return render(request,template_name="rec.html")