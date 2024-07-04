from django.shortcuts import render
from django.http import HttpResponse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

# Create your views here.

def index(request):
    return HttpResponse("You made it to the ultimate guitar backend!")

def login(request):
    loginURL = 'https://api-web.ultimate-guitar.com/v1/user/register/view'

    # Enable network logging
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'network': 'ALL'}

    # Set up Service
    service = Service(ChromeDriverManager().install())

    # Options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create chrome instance
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(loginURL)

    time.sleep(2000)

    return HttpResponse(200)