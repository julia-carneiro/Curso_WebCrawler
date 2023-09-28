import requests
from bs4 import BeautifulSoup

url = "https://steamcrackedgames.com/games/cracked"

response = requests.get(url)
text = BeautifulSoup(response.text, "html.parser")

td_cells = text.find_all("td")

for td in td_cells:
    a_tag = td.find("a", class_=["text-white", "text-secondary"])
    if a_tag:
        # Extrai os títulos
        if "text-white" in a_tag["class"]:
            titulo = a_tag.text.strip()
            # print("Título:", titulo)
        # Extrai os datas
        elif "text-secondary" in a_tag["class"]:
            data = a_tag.text.strip()
            # print("Data:", data)
