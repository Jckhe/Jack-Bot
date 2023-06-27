from dotenv import load_dotenv
import requests
import os
load_dotenv(override=False)
coin_token = os.environ.get('COIN_TOKEN')

def coinFetcher(coin):
    headers = {'X-CoinAPI-Key' : coin_token}
    coin = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
    coin = coin.json()
    print(coin['rate'])
    if (coin['rate'] < 1):
      return round(coin['rate'], 4)
    else:
      return round(coin['rate'], 2)
