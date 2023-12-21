from dotenv import load_dotenv
from dateutility import get_weekday_or_previous_friday
import requests
import json
import finnhub
import os
import hikari
load_dotenv(override=False)
finnhub_token = os.environ.get('FINNHUB_TOKEN')
finnhub_client = finnhub.Client(api_key=finnhub_token)
polygon_token = os.environ.get('POLYGON_TOKEN')

trading_day = get_weekday_or_previous_friday('America/Los_Angeles')
def polygon_query(ticker):
    return f"https://api.polygon.io/v1/open-close/{ticker}/{trading_day}?adjusted=true&apiKey={polygon_token}"

def stockFetcher(stock, message):
    embed = hikari.Embed(title=f"{stock} Price", description='', color="#FF0000")
    price = finnhub_client.quote(stock)
    print(price)
    embed.add_field(name="Current Price", value=f"${price['c']}", inline=True)
    embed.add_field(name="Change", value=price.get('d', 'N/A'), inline=True)
    embed.add_field(name="% Change", value=price.get('dp', 'N/A'), inline=True)
    embed.set_footer(text='yummy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')

    return embed

def afterHoursFetcher(stock, message):
    embed = stockFetcher(stock, message)
    polygon_fetch = requests.get(polygon_query(stock))
    polygon_response = json.loads(polygon_fetch.text)
    embed.add_field(name=f"After Hours ({trading_day})", value=f"{round(polygon_response['afterHours'], 2)}", inline=False)
    return embed