from django.shortcuts import render
from django.http import HttpResponse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

# Create your views here.

def index(request):
    return HttpResponse("You made it to the ultimate guitar backend!")

# def login(request):
    # TODO: implement some sort of login that uses the ultimate guitar tabs site
    # loginURL = 'https://api-web.ultimate-guitar.com/v1/user/register/view'

    # # Enable network logging
    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'network': 'ALL'}

    # # Set up Service
    # service = Service(ChromeDriverManager().install())

    # # Options
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # # Create chrome instance
    # driver = webdriver.Chrome(service=service, options=options)
    # driver.get(loginURL)

    # time.sleep(2000)

    # return HttpResponse(200)

def queryTabs(request):
    baseURL = 'https://www.ultimate-guitar.com/search.php?'
    value = request.GET.get('tabProp[value]')
    searchType = request.GET.get('tabProp[searchType]')
    page = request.GET.get('tabProp[page]')

    formattedURL = baseURL + 'page=' + page + '&search_type=' + searchType + '&value=' + value
    response = requests.get(formattedURL)
    html = response.text
    data = _getQueryResults(html)
    removedProTabs = []
    for elem in data:
        try:
            elem['marketing_type']
        except:
            removedProTabs.append(elem)
    return HttpResponse(json.dumps(removedProTabs))

def _getQueryResults(html):
    soup = BeautifulSoup(html)
    dataDiv = soup.find("div", {"class": "js-store"})
    data = json.loads(dataDiv['data-content'])
    return data['store']['page']['data']['results']