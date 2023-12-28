from dotenv import load_dotenv
import requests
import os
load_dotenv(override=False)
coin_token = os.environ.get('COIN_TOKEN')


priorityCoins = {
  'BTC': {'coinbase': True},
  'ETH': {'coinbase': True},
  'FET': {'coinbase': True},
}


def coinFetcher(coin):
    headers = {'X-CoinAPI-Key' : coin_token}
    response = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
    data = response.json()
    
    if 'error' in data:
      return False

    price = data['rate']

    if (price < 1):
      return round(price, 4)
    else:
      return round(price, 2)

#uses COINBASE API
def coinbaseFetcher(coin):
   response = requests.request("GET", f"https://api.coinbase.com/v2/prices/{coin}-USD/buy")
   data = response.json()
   print(data)
   if 'error' in data:
    return False
  
   price = float(data['data']['amount'])

   if price < 1:
    price = round(price, 4)
   else:
    price = round(price, 2)

   return price


  #check if coin is valid or check if its coinbase- if it is add it to the list
def coinChecker(coin):
  exists_on_coinbase = coinbaseFetcher(coin)

  if isinstance(exists_on_coinbase, (int, float)):
    priorityCoins[f"{coin.upper()}"] = {'coinbase': True}
    return
  
  exists_on_coinapi = coinFetcher(coin)

  if isinstance(exists_on_coinapi, (int, float)):
    priorityCoins[f"{coin.upper()}"] = {'coinbase': False}
    return
  else:
    return False
  

