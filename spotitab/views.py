from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from requests.models import PreparedRequest

spotifyAPI = "https://api.spotify.com/v1"

def index(request):
    return HttpResponse("Hello, world. You've made it to spotitab backend")

def setCodeVerifier(request, codeVerifier):
    request.session['codeVerifier'] = codeVerifier
    return HttpResponse(200)

def spCallback(request):
    code = request.GET.get('code')
    codeVerifier = request.session['codeVerifier']
    redirect_uri = 'http://localhost:8000/api/spcallback'

    payload = {
        'client_id': '9105a9e75db44212b7ec076f5763c85e',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': codeVerifier,
    }

    config = {
        'headers': {
            'content-type': 'application/x-www-form-urlencoded'
        },
    }

    try:
        response = requests.post("https://accounts.spotify.com/api/token", payload, config)
        data = response.json()

        request.session['accessToken'] = data['access_token']
        storeUserInfo(request, data['access_token'])
        return redirect('http://localhost:4200/view')
    except:
        return redirect('http://localhost:4200')
    
def storeUserInfo(request, accessToken):
    headers = {
        'Authorization': 'Bearer ' + accessToken
    }

    response = requests.get(spotifyAPI + "/me", headers = headers)
    data = response.json()

    request.session['userData'] = data
    
def getUsername(request):
    userData = request.session['userData']
    print(userData)

    return HttpResponse(userData['display_name'])
    
    
