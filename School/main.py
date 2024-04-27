import speech_recognition as sr
import random
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

random.seed()
random_number = random.randint(1,100)
print(f"RandomNumber {random_number}")

r = sr.Recognizer()

mic = sr.Microphone(device_index=0)

print("Start Speaking")

with mic as source:
	audio = r.listen(source)


try:
	result = r.recognize_google(audio)
except sr.RequestError:
	exit("API is unreachable")

except sr.UnknownValueError:
	exit("Unable to recognize speech! ")


with open(BASE_DIR+f'/SpeechHistory/{random_number}.txt',mode='w') as file:
	file.write(result)

print("It has stored speech into text in my file")

