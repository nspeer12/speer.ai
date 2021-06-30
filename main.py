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


@app.get('/query/{q}')
async def fulfillment(q:str):
	print(q)
	if q is not None:
		print(q)
		res = dex.process_input(q)
		print(res)
		return res
	else:
		return "hi i'm dexter"