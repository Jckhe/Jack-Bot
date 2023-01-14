import hikari
import requests
import os
from dotenv import load_dotenv
load_dotenv(override=False)
token = os.environ.get('TOKEN')
#intent
bot = hikari.GatewayBot(
    token,
    intents=hikari.Intents.ALL_UNPRIVILEGED  # Add this
    | hikari.Intents.MESSAGE_CONTENT,        # 
)

collections = []

def coinFetcher(coin):
    headers = {'X-CoinAPI-Key' : '9EE70F0D-01EE-42DD-A17A-C3808CE9580A'}
    coin = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
    coin = coin.json()
    return round(coin['rate'], 2)

def fetcher(slug):
    ##Fetch data from OS
    fetch_url = (f"https://api.opensea.io/api/v1/collection/{slug}/stats")
    headers = {"Accept": "application/json"}
    response = requests.request("GET", fetch_url, headers=headers)
    testdict = response.json()
    #Seperate each variable from the JSON
    #Floor Price
    unrounded_fp = (testdict['stats']['floor_price'])
    floor_price = round(unrounded_fp, 3)
    #One Day Volume
    unrounded_one_day_volume = (testdict['stats']['one_day_volume'])
    one_day_volume = round(unrounded_one_day_volume, 1)
    #Seven Day Volume
    unrounded_seven_day_volume = (testdict['stats']['seven_day_volume'])
    seven_day_volume = round(unrounded_seven_day_volume, 1)
    #Total Volume
    unroundedtotal_volume = (testdict['stats']['total_volume'])
    total_volume = round(unroundedtotal_volume, 1)
    #Supply and Holders
    unrounded_supply = (testdict['stats']['total_supply'])
    supply = int(unrounded_supply)
    holders = (testdict['stats']['num_owners'])
    #Holder Ratio
    unrounded_holder_ratio = (supply/holders)
    holder_ratio = round(unrounded_holder_ratio, 2)
    #URL Link
    os_url = (f"https://opensea.io/collection/{slug}")
    ##Embed for the data
    eth_suffix = " ETH"
    ## Image Fetcher
    os_thumbnail = image_fetcher(slug)
    ## TITLE fetcher
    os_title = title_fetcher(slug)
    ## ROYALTY FETCHER
    royalty = royalty_fetcher(slug)
    stats = (
        hikari.Embed(title=os_title, description='Click Above For Opensea', url=os_url, color="#FF0000")
        .add_field(name='Total Volume:', value=f"{total_volume} ETH", inline=True)
        .add_field(name='Total Supply:', value=supply, inline=True)
        .add_field(name='Number of Holders:', value=holders, inline=True)
        .add_field(name='Holder Ratio:', value=holder_ratio, inline=True)
        .add_field(name='Royalty Fee', value=royalty, inline=True)
        .add_field(name='**Floor Price**:', value=f"**{floor_price} ETH**")
        .set_footer(text='coded by Ky#0801', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
        .set_thumbnail(os_thumbnail)
    )
    return stats

##This function belows pulls the thumbnail image link from the OS collection
def image_fetcher(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    image_dict = response.json()
    final = (image_dict['collection']['primary_asset_contracts'][0]['image_url'])
    return final

##This function below pulls the TITLE of the collection
def title_fetcher(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    title_dict = response.json()
    final = (title_dict['collection']['primary_asset_contracts'][0]['name'])
    return final

def royalty_fetcher(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    royalty_dict = response.json()
    finale = (royalty_dict['collection']['primary_asset_contracts'][0]['seller_fee_basis_points'])
    final = str(finale)
    royalty_fee = ""
    if len(final) > 3:
        royalty_fee = f"{final[:2]}.{final[2:3]}%"
    else:
        royalty_fee = f"{final[:1]}.{final[1:2]}%"
    print(royalty_fee)
    return royalty_fee



@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:

    slug = ''
    if event.is_bot or not event.content:
        return
    if event.content.startswith("!j"):
        slug = (event.content[3:]).lower()
        print(slug)
        theslug = fetcher(slug)
        if theslug is KeyError:
            await event.message.respond("Unexpected error, try again.")
        else:
            await event.message.respond(theslug)
    if event.content.startswith("t"):
         coin = (event.content[2:]).upper()
         price = coinFetcher(coin)
         await event.message.respond(f"{coin} price is {price}")
    

# @bot.listen()
# async def ping(event: hikari.GuildMessageCreateEvent) -> None:
#     waifu_webhook = 969715882408439858
#     if event.author_id == waifu_webhook:
#         await bot.rest.create_message(962503723362431036, embed=event.embeds[0])
#         await bot.rest.create_message(921182971657060473, embed=event.embeds[0])

# ##DiedNFT 
# @bot.listen()
# async def ping(event: hikari.GuildMessageCreateEvent) -> None:
#     diednft = 953081479011913778
#     if event.author_id == diednft:
#         await bot.rest.create_message(962503723362431036, embed=event.embeds[0])
#         await bot.rest.create_message(976298974707347526, embed=event.embeds[0])

# ##Aoki
# @bot.listen()
# async def ping(event: hikari.GuildMessageCreateEvent) -> None:
#     aoki = 976311123441754132
#     if event.author_id == aoki:
#         await bot.rest.create_message(962503723362431036, embed=event.embeds[0])
#         await bot.rest.create_message(976257011975077938, embed=event.embeds[0])

# #MOBY
# @bot.listen()
# async def ping(event: hikari.GuildMessageCreateEvent) -> None:
#     my_channel_id = 982721287271096341
#     if event.channel_id == my_channel_id:
#         await bot.rest.create_message(962503723362431036, embed=event.embeds[0])
#         await bot.rest.create_message(982720466743619614, embed=event.embeds[0])



bot.run()
