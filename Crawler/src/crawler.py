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
        news = ul_element.find_all("li", {"class": "post"})

        all_data = []
        if news is None:
            if not retry:
                # time.sleep(3)
                self.extract_from_datasus(retry=True)
        else:
            for _news in news:
                titulo = _news.find("h2")
                resumo = _news.find("p")
                raw_data_publicacao = _news.find("span", class_="details")
                data_publicacao = raw_data_publicacao.text.strip().split(",")[0]
                link = _news.find("h2").find("a")

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
