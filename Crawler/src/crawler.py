import requests
from bs4 import BeautifulSoup
import time  # utilizado para retry da requisição
import textwrap  # besteira, apenas pra mostrar os textos inteiros, evitando que saiam da tela do console.
import schedule
from datetime import datetime
from database import DataBase
from dotenv import load_dotenv
import os
from bot import BOT


class Crawler:
    def __init__(self):
        load_dotenv()
        self.db = DataBase()
        self.bot = BOT()

    def request_data(self, url: str, retry: bool = False):
        """
        Faz uma requisição HTTP GET para a URL especificada e retorna o conteúdo em formato BeautifulSoup.

        :param url: A URL a ser requisitada.
        :return: O conteúdo da página web em formato BeautifulSoup.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            if not retry:
                time.sleep(3)
                return self.request_data(url, True)
            else:
                raise e
        return soup

    def post_twitter(self, data: dict):
        response = self.db.insert_db(data)
        if response is not None:
            self.bot.post(response)

    def extract_from_datasus(self, retry: bool = False, page: int = 1) -> None:
        """
        Extrai informações do site DATASUS.

        :param retry: Indica se a função deve tentar novamente em caso de falha na extração.
        """
        raw_datasus = self.request_data(
            "https://datasus.saude.gov.br/categoria/noticias/page/{}/".format(page)
        )

        # Pega lista
        ul_element = raw_datasus.find("ul", {"id": "posts-list"})
        # Encontra todas as notícias dentro da lista completa
        news_list = ul_element.find_all("li", {"class": "post"})

        # Lista para armazenar todas as notícias capturadas
        all_data = []

        if news_list is None:
            # caso seja None, e não tenha tentado novamente ainda - sleep(3) e tenta novamente.
            if not retry:
                time.sleep(3)
                self.extract_from_datasus(retry=True)
        else:
            # Percorre lista das notícias
            for news in news_list:
                titulo = news.find("h2")
                resumo = news.find("p")
                # Data sem formatação
                raw_data_publicacao = news.find("span", class_="details")
                data_publicacao = raw_data_publicacao.text.strip().split(",")[0]
                link = news.find("h2").find("a")

                # Dicionário com informações encontradas
                data = {
                    "titulo": titulo.text,
                    "resumo": resumo.text,
                    "data_publicacao": data_publicacao,
                    "link": link.attrs["href"],
                }
                # Salva todas as informações em uma lista
                all_data.append(data)

                # Insere DB e posta
                self.post_twitter(data)

    def extract_from_globo(self, retry: bool = False) -> None:
        """
        Extrai informações do site GLOBO - TUDO SOBRE SUS.

        :param retry: Indica se a função deve tentar novamente em caso de falha na extração.
        """
        raw_globo = self.request_data("https://g1.globo.com/tudo-sobre/sus/")

        # Lista de notícias
        news_list = raw_globo.find_all("div", class_="feed-post-body")

        all_data = []
        if news_list is None:
            if not retry:
                time.sleep(3)
                self.extract_from_datasus(retry=True)
        else:
            for news in news_list:
                titulo = news.find("h2")
                resumo = news.find("div", class_="feed-post-body-resumo")
                raw_data_publicacao = news.find("span", class_="feed-post-datetime")
                data_publicacao = raw_data_publicacao.text.strip().split(",")[0]
                link = news.find("h2").find("a")

                data = {
                    "titulo": titulo.text,
                    "resumo": resumo.text,
                    "data_publicacao": data_publicacao,
                    "link": link.attrs["href"],
                }

                all_data.append(data)

                self.post_twitter(data)

    def execute(self, num_pages: int = 1):
        for page in range(1, num_pages):
            self.extract_from_datasus(page)
        self.extract_from_globo(page)
        exit()


if __name__ == "__main__":
    crawler = Crawler()
    crawler.execute(2)

    def job():
        print("\nExecute job. Time {}".format(str(datetime.now())))
        crawler.execute()

    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
