import hikari
import requests
import os
from dotenv import load_dotenv
from nft import fetcher
from crypto import coinFetcher
from stocks import stockFetcher
load_dotenv(override=False)
discord_token = os.environ.get('TOKEN')


#intent
bot = hikari.GatewayBot(
    discord_token,
    intents=hikari.Intents.ALL_UNPRIVILEGED  # Add this
    | hikari.Intents.MESSAGE_CONTENT,        # 
)

# def coinFetcher(coin):
#     headers = {'X-CoinAPI-Key' : coin_token}
#     coin = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
#     coin = coin.json()
#     return round(coin['rate'], 2)

# def fetcher(slug):
#     """Fetch data from OpenSea API."""
#     fetch_url = f"https://api.opensea.io/api/v1/collection/{slug}/stats"
#     headers = {"Accept": "application/json"}
#     response = requests.get(fetch_url, headers=headers)
#     data = response.json()

#     # Extract and process data from the JSON response
#     stats = data['stats']
#     floor_price = round(stats['floor_price'], 3)
#     one_day_volume = round(stats['one_day_volume'], 1)
#     seven_day_volume = round(stats['seven_day_volume'], 1)
#     total_volume = round(stats['total_volume'], 1)
#     supply = int(stats['total_supply'])
#     holders = stats['num_owners']
#     holder_ratio = round(supply / holders, 2)

#     # Fetch additional data
#     os_url = f"https://opensea.io/collection/{slug}"
#     os_thumbnail = image_fetcher(slug)
#     os_title = title_fetcher(slug)
#     royalty = royalty_fetcher(slug)

#     # Create embed for the data
#     embed = hikari.Embed(title=os_title, description='Click Above For Opensea', url=os_url, color="#FF0000")
#     embed.add_field(name='Total Volume:', value=f"{total_volume} ETH", inline=True)
#     embed.add_field(name='Total Supply:', value=supply, inline=True)
#     embed.add_field(name='Number of Holders:', value=holders, inline=True)
#     embed.add_field(name='Holder Ratio:', value=holder_ratio, inline=True)
#     embed.add_field(name='Royalty Fee', value=royalty, inline=True)
#     embed.add_field(name='**Floor Price**:', value=f"**{floor_price} ETH**")
#     embed.set_footer(text='coded by Ky#0801', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
#     embed.set_thumbnail(os_thumbnail)

#     return embed




@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:

    slug = ''
    if event.is_bot or not event.content:
        return
    # if event.content.startswith("!j"):
    #     slug = (event.content[3:]).lower()
    #     print(slug)
    #     theslug = fetcher(slug)
    #     if theslug is KeyError:
    #         await event.message.respond("Unexpected error, try again.")
    #     else:
    #         await event.message.respond(theslug)
    if event.content.startswith("t"):
         message = (event.content[2:]).upper()
         coins = message.split(" ")
         print("coin: ", coins)
         response = ""
         for coin in coins:
            price = coinFetcher(coin)
            response += f"**{coin}**: ${price}\n"
         await event.message.respond(response)
    if event.content.startswith("p"):
        message = (event.content[2:]).upper()
        # print("stocks: ", message)
        # price = finnhub_client.quote(message)
        # print("price: ", price)
        # output = (
        #     hikari.Embed(title=f"{message} price", description='', color="#FF0000")
        #     .add_field(name="Current Price: ", value=f"${price['c']}", inline=True)
        #     .add_field(name="Change", value=price['d'], inline=True)
        #     .add_field(name="% Change", value=price['dp'], inline=True)
        #     .set_footer(text='yammy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
        # )
        await event.message.respond(stockFetcher(message))
        

bot.run()
