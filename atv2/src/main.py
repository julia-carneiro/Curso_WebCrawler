import requests
from bs4 import BeautifulSoup

# parei no minuto 45:40

# 1 Kabum - consoles
# https://www.kabum.com.br/gamer?page_number=1&page_size=20&facet_filters=&sort=most_searched

response = requests.get("https://www.kayak.com.br/explore/FEC-anywhere")
text = BeautifulSoup(response.text, "html.parser")

name = text.findAll("div", {"class": "City__Name"})


print(name)


# 2 Google Flights
#  https://www.google.com/travel/explore?tfs=CBwQAxoPag0IAxIJL20vMDl3d2xqGg9yDQgDEgkvbS8wOXd3bGpAAUgBcAKCAQsI____________AZgBAbIBBBgBIAE&tfu=GgAqAggD


# 3
