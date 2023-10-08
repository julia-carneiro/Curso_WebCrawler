import requests
from bs4 import BeautifulSoup
import time


class Crawler:
    def request_data(self, url: str):
        """
        Faz uma requisição HTTP GET para a URL especificada e retorna o conteúdo em formato BeautifulSoup.

        :param url: A URL a ser requisitada.
        :return: O conteúdo da página web em formato BeautifulSoup.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def imprime_infos(self, site: str, data: dict):
        """
        Imprime as informações formatadas de um site específico.

        :param site: O nome do site.
        :param data: Um dicionário contendo as informações a serem impressas.
        """
        print("\n***", site, "***\n")
        print("Título:", data["titulo"])
        print("Resumo:", data["resumo"])
        print("Data de publicação:", data["data_publicacao"])
        print("Link:", data["link"])
        print("---------------------")

    def extract_from_datasus(self, retry: bool = False) -> None:
        """
        Extrai informações do site DATASUS.

        :param retry: Indica se a função deve tentar novamente em caso de falha na extração.
        """
        raw_datasus = self.request_data(
            "https://datasus.saude.gov.br/categoria/noticias/"
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
            # Printa APENAS UMA DAS NOTÍCIAS PARA TESTE
            self.imprime_infos("DATASUS", data)

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
            self.imprime_infos("GLOBO - TUDO SOBRE SUS", data)


if __name__ == "__main__":
    crawler = Crawler()
    # Extrai informações do site DATASUS
    crawler.extract_from_datasus()
    # Extrai informações do site GLOBO - TUDO SOBRE SUS
    crawler.extract_from_globo()
