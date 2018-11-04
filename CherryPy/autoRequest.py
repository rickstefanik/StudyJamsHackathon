#! /usr/bin/env python3

import requests
import json

URL = "https://0a2aa408.ngrok.io"
print(requests.post(URL, json.dumps({"text": "Study Jams is the best application for memorization."})).content)
