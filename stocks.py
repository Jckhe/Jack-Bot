from dotenv import load_dotenv
import requests
import finnhub
import os
import hikari
load_dotenv(override=False)
finnhub_token = os.environ.get('FINNHUB_TOKEN')
finnhub_client = finnhub.Client(api_key=finnhub_token)

def stockFetcher(stock):
  price = finnhub_client.quote(stock)
  output = (
    hikari.Embed(title=f"{stock} price", description='', color="#FF0000")
    .add_field(name="Current Price: ", value=f"${price['c']}", inline=True)
    .add_field(name="Change", value=price['d'], inline=True)
    .add_field(name="% Change", value=price['dp'], inline=True)
    .set_footer(text='yammy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
    )
  return output
