import os
from os import path
import speech_recognition as sr
import datetime
import time
from multiprocessing import Process
from scipy.io.wavfile import write
from playsound import playsound
import csv
import torch
import torch.nn as nn
import speech_recognition
import nltk
from nltk.stem import WordNetLemmatizer
import wave
import numpy as np
import pvporcupine
import pyaudio
import struct

# gotta back that shit up for imports to work
import sys
sys.path.append("..")

from assistant.skills import *
from assistant.utils.intro import intro
from assistant.model.assistantModel import NeuralNet
from assistant.nlp import *



MIC_SOURCE = 1
WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]





class DexterCloud:

	def __init__(self, debug=False):
		self.startup = time.time()
		self.debug = debug
		self.cwd = os.getcwd()

		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		# Define CSV paths
		dir_name = path.dirname(__file__)

		path.join(dir_name, 'csv/gesture_label.csv')

		ASSISTANT_PATH = path.join(dir_name, "model/AssistantModel.pth")
		FEATURES_PATH = path.join(dir_name, "model/Assistant_features.csv")
		LABELS_PATH = path.join(dir_name, "model/Assistant_labels.csv")

		# read in csv for num features and classes
		with open(FEATURES_PATH) as f:
			reader = csv.reader(f)
			Assistant_features = [row[0] for row in reader]

		self.num_features = len(Assistant_features)

		self.feature_dict = {}
		for i in range(self.num_features):
			self.feature_dict[Assistant_features[i]] = i

		with open(LABELS_PATH) as f:
			reader = csv.reader(f)
			self.Assistant_labels = [row[0] for row in reader]
		
		self.num_classes = len(self.Assistant_labels)

		self.model = NeuralNet(self.num_features,self.num_classes)
		self.model.load_state_dict(torch.load(ASSISTANT_PATH, map_location=self.device))
		self.model.eval()
		
		if self.debug:
			print("loaded assistant model")


		self.mappings = {
			'greeting' : greeting,
			'introduction' : introduction,
			'goodbye' : goodbye,
			'wiki' : wiki,
			'math' : math,
			'news' : news,
			'date' : date,
			'time' : get_time,
			'day' : day,
			'question' : question,
      		'weather' : weather,
			'bitcoin_price' : bitcoin_price,
			'convo' : convo,
			'print_chat_log' : print_chat_log,
		}

		self.context = ""

		self.query_history = []
		self.response_history = []

	def get_input(self):
		# get input from microphone -> google api -> text
		while True:
			try:
				with speech_recognition.Microphone() as mic:
					self.recognizer.adjust_for_ambient_noise(mic,duration=0.2)
					audio = self.recognizer.listen(mic)
					text = self.recognizer.recognize_google(audio)
					text = text.lower()
					print(f"You said:\n{text}")
					if (text != ""):
						self.message = text
						return text
					else:
						print("empty string")
			except Exception as ex:
				print(ex)


	def process_input(self, text):
		text = clean_text(text)

		bag = [0] * self.num_features
		words = nltk.word_tokenize(text)
		for word in words:
			if word.lower() in self.feature_dict:
				bag[self.feature_dict[word.lower()]] += 1

		bag = torch.from_numpy(np.array(bag))
		# print(bag)
		output = self.model.forward(bag.float())

		prediction = self.Assistant_labels[torch.argmax(output)]


		if prediction in self.mappings.keys():

			res = self.mappings[prediction](text, self.context)
			if res != None:
				self.query_history.append(text)
				self.response_history.append(res)

				self.context += 'Human: ' + text + '\n'
				self.context += 'AI: ' + res + '\n'
				return res


	def listen(self):
		
		#playsound('sounds/boing.wav')
		
		run = True


		print('Listening...')


		with sr.Microphone() as source:
			
			#self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
			
		
			try:
				recorded_audio = self.recognizer.listen(source, timeout=1)
				
				print("Recognizing")

				start = time.time()

				text = self.recognizer.recognize_google(
						recorded_audio,
						language='en-US')

			except Exception as ex:
				if self.debug:
					print(ex)

			else:
				
				decode_time = time.time() - start

				if self.debug:
					print("Detection time: {}".format(decode_time))

				'''
				with open('logs/decode-time.txt', 'a') as decode:
					decode.write("{}\n".format(decode_time))
					decode.close()
				'''

				if self.debug:
					print("Decoded Text : {}".format(text))

											
				self.process_input(text)

				if self.debug:
					print("Total Response Time: {}\n".format(time.time() - start))

				'''
				with open('logs/total-response-time.txt', 'a') as trt:
					trt.write("{}\n".format(time.time() - start))
					trt.close()
				'''

		return
