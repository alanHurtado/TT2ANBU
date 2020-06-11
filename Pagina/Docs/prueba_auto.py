import requests
import time

from os import listdir
from os.path import isfile, join

mypath = "./detections"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
# initialize the Keras REST API endpoint URL along with the input
# image path
API_URL = "http://0.0.0.0:8000/detections/56"

# load the input image and construct the payload for the request
for img in onlyfiles:
	IMAGE_PATH = mypath + "/" + img
	print(IMAGE_PATH)
	image = open(IMAGE_PATH, "rb").read()
	payload = {"images": image}
	r = requests.post(API_URL, files=payload).json()
	print(r)
