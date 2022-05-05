import hikari
import requests

# Hi Opensea Devs, this is a very simple discord bot I developed from scratch!

#Discord Bot Token
bot = hikari.GatewayBot(token='')

collections = []

#This fetcher function is used to send a request to the Opensea API and retrieve said collection stats.
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
    stats = (
        hikari.Embed(title=slug, description='Click for Opensea', url=os_url, color="#FF0000")
        .add_field(name='1-Day Volume:', value=f"{one_day_volume} ETH", inline=True)
        .add_field(name='7-Day Volume:', value=f"{seven_day_volume} ETH", inline=True)
        .add_field(name='Total Volume:', value=f"{total_volume} ETH", inline=True)
        .add_field(name='Total Supply:', value=supply, inline=True)
        .add_field(name='Number of Holders:', value=holders, inline=True)
        .add_field(name='Holder Ratio:', value=holder_ratio, inline=True)
        .add_field(name='**Floor Price**:', value=f"**{floor_price} ETH**")
        .set_footer(text='coded by Ky#0801', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
    )
    return stats

#This function is used to ping when a user starts a message with: !j , the bot saves the slug following the command and then sends to the function above ^ which then is used to retrieve the said stats and is pinged back in an EMBED message.
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

    
#Used to run the bot
bot.run()
