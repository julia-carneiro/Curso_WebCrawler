from pymongo import MongoClient
from dotenv import load_dotenv
import os


class DataBase:
    def __init__(self):
        load_dotenv()
        self.noticias = self.connect_db()

    def connect_db(self):
        client = MongoClient(os.getenv("DB_URI"))
        db = client["CursoCrawler"]
        return db.noticias

    def insert_db(self, data: dict):
        query = {"titulo": data["titulo"]}
        result = self.noticias.find_one(query)
        if result is None:
            self.noticias.insert_one(data)
            print("Inserido com sucesso")
            return data
        else:
            print("Os dados já existem no banco de dados.")
            return None

    def find_data(self, query: dict):
        result = self.noticias.find_one(query)
        if result:
            print("Dados encontrados:")
            print(result)
        else:
            print("Dados não encontrados no banco de dados.")


if __name__ == "__main__":
    db = DataBase()
    data = {
        "titulo": "Sol Nascente: moradores da maior favela do país demoram 1h30 para chegar ao hospital mais próximo",
        "resumo": "Região com 32.081 domicílios conta com apenas uma UBS. Mães da 'Fazendinha' enfrentam caminhada de 30 minutos e cerca de uma hora entre espera pelo ônibus e chegada ao Hospital Regional de Ceilândia, no Distrito Federal.",
        "data_publicacao": "Há 2 dias",
        "link": "https://g1.globo.com/df/distrito-federal/noticia/2023/10/13/sol-nascente-moradores-da-maior-favela-do-pais-demoram-1h30-para-chegar-ao-hospital-mais-proximo.ghtml",
    }
    data2 = {
        "titulo": "PEC pretende liberar a comercialização de plasma humano no Brasil",
        "resumo": "A Comissão de Constituição e Justiça do Senado pode analisar nesta quarta-feira (4) uma proposta de emenda à Constituição que muda as regras para coleta e processamento de plasma humano.",
        "data_publicacao": "Há 2 semanas",
        "link": "https://g1.globo.com/jornal-nacional/noticia/2023/10/03/pec-pretende-liberar-a-comercializacao-de-plasma-humano-no-brasil.ghtml",
    }
    print("Inserindo novo elemento:")
    db.insert_db(data2)
    print("\nInserindo elemento já existente:")
    db.insert_db(data)

    # Exemplo: Buscar dados pelo título
    query = {
        "titulo": "Sol Nascente: moradores da maior favela do país demoram 1h30 para chegar ao hospital mais próximo"
    }
    db.find_data(query)
