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

totalTabNum = 0

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
    value = request.GET.get('value')
    searchType = request.GET.get('search_type')
    page = request.GET.get('page')

    formattedURL = baseURL + 'page=' + page + '&search_type=' + searchType + '&value=' + value
    response = requests.get(formattedURL)

    html = response.text

    totalTabNum = _findTotalTabNumber(html)

    data = _getQueryResults(html)

    removedProTabs = [[totalTabNum]]
    for elem in data:
        try:
            elem['marketing_type']
        except:
            if (elem['type'] != 'Pro'):
                removedProTabs.append(elem)
    return HttpResponse(json.dumps(removedProTabs))

def _findTotalTabNumber(html):
    soup = BeautifulSoup(html, features="lxml")

    titleString = str(soup.find("title"))
    
    titleList = titleString.split(" ")
    indexOfChords = titleList.index("&amp;")
    totalTabs = titleList[indexOfChords - 2]

    return int(totalTabs)

def _getQueryResults(html):
    soup = BeautifulSoup(html, features="lxml")

    dataDiv = soup.find("div", {"class": "js-store"})
    data = json.loads(dataDiv['data-content'])

    return data['store']['page']['data']['results']

def getTabInfo(request):
    tabURL = request.GET.get('tabURL')

    response = requests.get(tabURL)
    html = response.text
    raw_data = _getHTMLTabData(html)
    print(json.dumps(raw_data))
    return HttpResponse(json.dumps(raw_data))

def _getHTMLTabData(html):
    soup = BeautifulSoup(html)
    dataDiv = soup.find("div", {"class": "js-store"})
    data = json.loads(dataDiv['data-content'])
    tabDict = {
        'tabText': data['store']['page']['data']['tab_view']['wiki_tab']['content'],
        'artistName': data['store']['page']['data']['tab']['artist_name'],
        'songName': data['store']['page']['data']['tab']['song_name'],
        'songUrl': data['store']['page']['data']['tab']['tab_url']
    }
    return tabDict

def getTotalTabNum(request):
    return HttpResponse(request.session['totalTabs'])