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
        news = raw_datasus.find_all("ul", {"id": "posts-list"})
        # print(news)
        if news is None:
            if not retry:
                # time.sleep(3)
                self.extract_from_datasus(retry=True)
        else:
            for _news in news:
                image = _news.find("img", {"class": "img-fluid"})
                titulo = _news.find("h2")
                resumo = _news.find("p")
                data_publicacao = (
                    _news.find("span", class_="details").text.strip().split(",")[0]
                )
                link = _news.find("h2").find("a")
            data = {
                "image": image.attrs["src"],
                "titulo": titulo.text,
                "resumo": resumo.text,
                "data_publicacao": data_publicacao,
                "link": link.attrs["href"],
            }
            print(data)
        # print(news)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_datasus()
