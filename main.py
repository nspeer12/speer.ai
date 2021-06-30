import time
import threading
import multiprocessing
import time
from fastapi import FastAPI, Request
import requests
import json
import os
from settings import *
from assistant import *


app = FastAPI()

dex = DexterCloud(debug=True)



@app.get('/')
async def index():
	return 'dexter ai'



@app.get('fulfillment/{messsage}')
async def fulfillment(message:str):
	print('here')
	if message is not None:
		print('message: ' + message)
		res = dex.process_input(message)
		print(res)
		return res


		
'''
@app.post('/voice-settings')
def voice_settings():
	return ''


@app.post('/train-assistant')
def train_assistant():
	os.chdir('assistant/model/')
	from trainAssistant import train_assistant
	train_assistant()
	os.chdir('..')
	os.chdir('..')
	return 'level up'
'''