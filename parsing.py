import requests
from bs4 import BeautifulSoup
import fake_useragent

fakeUser = fake_useragent.UserAgent().random
headers = {'user-agent':fakeUser}

user_music = "пьяный"
url = "https://muzati.net/search/?q=" + user_music
response = requests.get(url, headers = headers).text

response = BeautifulSoup(response,"lxml")
print(response.title)