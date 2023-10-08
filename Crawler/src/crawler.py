import requests
from bs4 import BeautifulSoup
import time
import os


class Crawler:
    def request_data(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def extract_from_datasus(self, page: int = 1, retry: bool = False) -> None:
        raw_datasus = self.request_data(
            "https://datasus.saude.gov.br/categoria/noticias/"
        )
        ul_element = raw_datasus.find("ul", {"id": "posts-list"})
        news_list = ul_element.find_all("li", {"class": "post"})

        all_data = []
        if news_list is None:
            if not retry:
                # time.sleep(3)
                self.extract_from_datasus(retry=True)
        else:
            for news in news_list:
                titulo = news.find("h2")
                resumo = news.find("p")
                raw_data_publicacao = news.find("span", class_="details")
                data_publicacao = raw_data_publicacao.text.strip().split(",")[0]
                link = news.find("h2").find("a")

                data = {
                    "titulo": titulo.text,
                    "resumo": resumo.text,
                    "data_publicacao": data_publicacao,
                    "link": link.attrs["href"],
                }
                all_data.append(data)
            # print(all_data)

    def extract_from_globo(self):
        raw_globo = self.request_data("https://g1.globo.com/tudo-sobre/sus/")
        news_list = raw_globo.find_all("div", class_="feed-post-body")

        all_data = []
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
        # print(all_data)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_datasus()
    crawler.extract_from_globo()
