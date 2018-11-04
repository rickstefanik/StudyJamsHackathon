#! /usr/bin/env python3

import requests
import json

URL = "http://a2ff62f7.ngrok.io/"
print(requests.post(URL, json.dumps({"text": "Study Jams is awesome.  Study Jams is awesome."})).content)
