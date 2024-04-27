from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *
from django.http import HttpResponse
from datetime import datetime, timedelta
import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#C:\Users\DIMOSO JR\Desktop\ProjectWork\SmartInvigilation\SmartInvigilationProject\SmartInvigilationApp
print(BASE_DIR)
from django.core.files.base import ContentFile


#@login_required(login_url='login')
def home(request):
    speech_text = request.session.get('speech_text', '')

    return render(request,'App/home.html', {'speech_text': speech_text})


@login_required(login_url='login')
def starting_page(request):


    return render(request, 'App/starting_page.html')

@login_required(login_url='login')
def all_speeches(request):
    user = request.user.username
    speeches = SpeechRecognitionHistory.objects.filter(
        username__icontains = user
        ).order_by('-id')

    context = {
        "speeches":speeches,
    }

    return render(request, 'App/all_speeches.html',context)


@login_required(login_url='login')
def speech_recognition(request):
    error_message =None
    

    if request.method == 'POST':

        random.seed()
        random_number = random.randint(1,100)
        print(f"RandomNumber {random_number}")

        username = request.user.username
        email = request.user.email
        microphone_no = 0 #request.POST.get('microphone_no')

        save_speech = SpeechRecognitionHistory.objects.create(username=username, email=email)
        save_speech.save()

        # microphone_no_integer = int(microphone_no)



        


        #START SPEECH RECOGNITION
        import speech_recognition as sr

        r = sr.Recognizer()

        mic = sr.Microphone(device_index=microphone_no)

        print("Start Speaking")
        #error_message = "Start Speaking!!"
        #messages.info(request, f'Hey {username} Start Speaking')


        with mic as source:
            audio = r.listen(source)


        try:
            result = r.recognize_google(audio)
        except sr.RequestError:
            #exit("API is unreachable")
            #error_message = "API is unreachable"
            messages.info(request, f'Hey {username}, Requested API is unreachable')
            return redirect("home")


        except sr.UnknownValueError:
            #exit("Unable to recognize speech! ")
            #error_message = "Unable to recognize speech!"
            messages.info(request, f'Hey {username}, Unable to recognize speech!')
            return redirect("home")


        with open(BASE_DIR+f'\\SpeechHistory\\my_speech.txt',mode='w') as file:
            file.write(result)

        print("It has stored speech into text in my file")
        #error_message = "It has stored speech into text in my file"
        messages.info(request, f'Hey {username}, It has stored speech into text in my file')


        # Save speech text file to the model
        with open(BASE_DIR+f'\\SpeechHistory\\my_speech.txt', 'rb') as file:
            save_speech.speech_files.save('my_speech.txt', ContentFile(file.read()), save=True)


        # Delete the temporary file
        # os.remove(BASE_DIR+f'\\SpeechHistory\\my_speech.txt')
        

        # Reading speech from text file
        with open(BASE_DIR+f'\\SpeechHistory\\my_speech.txt', mode='r') as file:
            speech_text = file.read()

        # Printing speech in terminal
        print("Speech from file:")
        print(speech_text)

        # Storing speech in a variable to use later
        request.session['speech_text'] = speech_text




        return redirect("home")


            

    # context = {
    #     "error_message":error_message,
    # }

    # return render(request,'App/home.html',context)