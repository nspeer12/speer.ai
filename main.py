import time
import threading
import multiprocessing
import time
from fastapi import FastAPI, Request, Query
import requests
import json
import os
from settings import *
from assistant import *


app = FastAPI()

dex = DexterCloud(debug=True)


@app.get('/')
async def index():
	return 'dexter'


@app.get('/query/{query}')
async def fulfillment(query:str):
	print(query)
	if query is not None:
		print(query)
		res = dex.process_input(query)
		print(res)
		return res
	else:
		return "hi i'm dexter"