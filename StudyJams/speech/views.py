from django.shortcuts import render
import requests
import json
import time
from django.views.decorators.cache import never_cache

@never_cache
def index(request):

    URL = "0a2aa408.ngrok.io/"
    if 'textToSpeak' in request.GET:
        print("I'm in the GET")
        sayThis = request.GET.get('textToSpeak')
        print(str(sayThis))
        r = requests.post("https://" + URL, json.dumps({"text": str(sayThis)}))
        #print(r.text)
    
    time.sleep(10)
    return render(request, "speech/index.html")

# Create your views here.
