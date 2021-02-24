import pyttsx3
import speech_recognition as sr
import datetime
from skills import *
import time
from multiprocessing import Process
from voice import *
from _wikipedia_api import *
from _wolfram_api import *
from nlp import *
import sounddevice as sd
from scipy.io.wavfile import write
from nlp import *


MIC_SOURCE = 2
WAKE_WORDS = ["Dexter", "hey Dexter", "ok computer", "Okay computer" "hey computer", "dex"]

def get_voices():
	voices = engine.getProperty('voices')
	for voice in voices:
		print(voice, voice.id)
		engine.setProperty('voice', voice.id)
		engine.say("Hello World!")
		engine.runAndWait()
		engine.stop()


def listen_for_wake():
	sleep = True

	with sr.Microphone(MIC_SOURCE) as source:
		recognizer.adjust_for_ambient_noise(source, duration=2)
		while sleep:
			try:
				print("Waiting for wake word")
				recorded_audio = recognizer.listen(source, timeout=1)
				print("Recognizing")
				start = time.time()

				text = recognizer.recognize_google(
						recorded_audio, 
						language="en-US"
					)
				print("Detection time: {}".format((time.time() - start)))
				print("Decoded Text : {}".format(text))
			except Exception as ex:
				print(ex)
				continue

			for word in WAKE_WORDS:
				if word.lower() in text.lower():
					handle_query(text)
					break


def record_audio():
	with sr.Microphone(MIC_SOURCE) as source:
		print("Recording for 4 seconds")
		recorded_audio = recognizer.listen(source, timeout=4)
		print(recorded_audio)
		print("Done recording")
	try:
		print("Recognizing the text")
		text = recognizer.recognize_google(
				recorded_audio, 
				language="en-US"
			)
		print("Decoded Text : {}".format(text))

	except Exception as ex:
		print(ex)

def speak(text:str):
	engine.say(text)
	engine.runAndWait()


def handle_query(query:str):
	query = clean_query(query)

	# call function based on query
	keys = skills_map.keys()
	for key in keys:
		if key in query.lower():
			print(key)
			reply = skills_map[key]()
			if reply != '':
				voice(reply)
			return
	
	# not a skill, ask wikipedia or wolfram
	voice(ask_wolfram(query))


if __name__ == '__main__':
	engine = pyttsx3.init()
	recognizer = sr.Recognizer()
	voice("Hello sir, my name is Dexter, you're virtual assistant. How can I help you.")
	listen_for_wake()

	#engine.say("Howdy, my name is Dexter. How can I help.")
	#listen_for_wake()

	