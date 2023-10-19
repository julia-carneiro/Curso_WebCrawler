import tweepy
from dotenv import load_dotenv
import os


class BOT:
    def __init__(self):
        load_dotenv()
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_key_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        bearer_token = os.getenv("BEARER_TOKEN")

        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
        )

        # Apenas para imagens
        # auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        # auth.set_access_token(
        #    access_token,
        #    access_secret
        # )

        # self.api = tweepy.API(auth)

    def post(self, data: dict):
        try:
            # Havia feito um calculo para redução do tamanho do resumo caso excedesse 280 caracteres porém não ficou muito interessante,
            # muitas vezes o resumo ficava muito pequeno e sem sentido,
            # por isso decidi deixar apenas o título

            # Cria texto do tweet
            tweet_text = "{}\n\nData: {}\n\nLink: {}".format(
                data["titulo"],
                data["data_publicacao"],
                data["link"],
            )

            self.client.create_tweet(text=tweet_text)
            return True

        except Exception as e:
            print(str(e))
            return False
