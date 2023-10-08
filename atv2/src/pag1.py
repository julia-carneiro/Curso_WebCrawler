import requests
from bs4 import BeautifulSoup

# URL da página que deseja analisar
url = "https://datasus.saude.gov.br/categoria/noticias/"

# Faz uma solicitação HTTP para obter o conteúdo da página
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parseia o conteúdo HTML da página com BeautifulSoup
    text = BeautifulSoup(response.text, "html.parser")

    # Encontre todos os elementos que contêm informações de notícias
    news_elements = text.find_all("div", class_="col-9")

    # Itera sobre cada elemento de notícia e extrai as informações
    for news_element in news_elements:
        # Extraia o título
        titulo = news_element.find("h2").text.strip()

        # Extraia o resumo
        resumo = news_element.find("p").text.strip()

        # Extraia a data de publicação
        data_element = news_element.find("span", class_="details")
        data = data_element.text.strip().split(",")[0]  # Pega apenas a parte da data

        # Imprima as informações de cada notícia
        print("Título:", titulo)
        print("Resumo:", resumo)
        print("Data de Publicação:", data)
        print("---")  # Separador entre as notícias

else:
    print("Falha ao acessar a página. Código de status:", response.status_code)
