from dotenv import load_dotenv
from date_handlers.date_functions import yesterdayTimeString
import requests
import os
load_dotenv(override=False)
coin_token = os.environ.get('COIN_TOKEN')


priorityCoins = {
  'BTC': {'coinbase': True},
  'ETH': {'coinbase': True},
  'FET': {'coinbase': True},
}

derekCoins = {
  'BTC': {'coinbase': True},
  'ETH': {'coinbase': True},
}


def coinFetcher(coin):
    headers = {'X-CoinAPI-Key' : coin_token}
    response = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
    data = response.json()
    
    if 'error' in data:
      return False
    print(f"data: {data}")
    price = data['rate']

    if (price < 1):
      return round(price, 4)
    else:
      return round(price, 2)

#uses COINBASE API
def coinbaseFetcher(coin):
   response = requests.request("GET", f"https://api.coinbase.com/v2/prices/{coin}-USD/buy")
   data = response.json()

   if 'error' in data:
    return False

   price = float(data['data']['amount'])
   print(f"data cb: {data}")

   if price < 1:
    price = round(price, 4)
   else:
    price = round(price, 2)

   return price




# Calculates the 24 hour % change (Prototype)
def percentageChange(currentPrice, coin):
  time = yesterdayTimeString()
  print(f"time: {time}")
  headers = {'X-CoinAPI-Key' : coin_token}
  response = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/usd?time={time}", headers=headers)
  data = response.json()
  print(f"data %: {data}")
  if 'error' in data:
    return ""
  
  oldPrice = data['rate']
  print(f"Old Price: {oldPrice} and newPrice: {currentPrice}")
  change = ((currentPrice- oldPrice) / abs(oldPrice)) * 100
  change_symbol = '+' if change >= 0 else '-'

  return f"{change_symbol}{abs(change):.2f}%"



  #check if coin is valid or check if its coinbase- if it is add it to the list
def coinChecker(coin, watchlist=priorityCoins):
  exists_on_coinbase = coinbaseFetcher(coin)

  if isinstance(exists_on_coinbase, (int, float)):
    watchlist[f"{coin.upper()}"] = {'coinbase': True}
    return
  
  exists_on_coinapi = coinFetcher(coin)

  if isinstance(exists_on_coinapi, (int, float)):
    watchlist[f"{coin.upper()}"] = {'coinbase': False}
    return
  else:
    return False
  

def messageCreator(coins, response):
  for coin in coins:
    price = coinbaseFetcher(coin)
    
    if price != False:
      percentage = percentageChange(price, coin)
      response += f"**{coin}**: ${price}  `{percentage}` \n"
    else:
      price = coinFetcher(coin)
      percentage = percentageChange(price, coin)
      if price != False:
        response += f"**{coin}**: ${price}  `{percentage}` \n"
      else:
        response += f"**{coin}**: Can't find coin on coinbase or coinapi\n"
    
  return response