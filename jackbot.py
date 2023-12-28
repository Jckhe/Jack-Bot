import hikari
import requests
import os
from dotenv import load_dotenv
from nft import fetcher
from crypto import coinFetcher, priorityCoins, coinbaseFetcher, coinChecker
from stocks import stockFetcher, afterHoursFetcher
load_dotenv(override=False)
discord_token = os.environ.get('TOKEN')
admin_token=os.environ.get('ADMIN')


#intent
bot = hikari.GatewayBot(
    discord_token,
    intents=hikari.Intents.ALL_UNPRIVILEGED  # Add this
    | hikari.Intents.MESSAGE_CONTENT,        # 
)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content and event.content.startswith("!t"):
        if (len(event.content) == 2):
            response = "Watchlist: \n"
            for coin, details in priorityCoins.items():
                on_coinbase = details.get('coinbase', False)
                if on_coinbase:
                    price = coinbaseFetcher(coin)
                    response += f"**{coin}**: ${price}\n"
                else:
                    price = coinFetcher(coin)
                    response += f"**{coin}**: ${price}\n"
            await event.message.respond(response)    
        if len(event.content) > 2:
            if event.content[3:6] == 'add':
                coinsToAdd = event.content[7:]
                print("coins to add: ", coinsToAdd)
                if not coinsToAdd:
                    await event.message.respond("No coins given") 
                    return
                coinsToAdd = coinsToAdd.split(" ")
                print("coins to add: ", coinsToAdd)
                for coin in coinsToAdd:
                    print("coin: ", coin)
                    if coin in priorityCoins:
                        await event.message.respond(f"{coin} already exists.")
                        continue
                    else:
                        coinCheck = coinChecker(coin)
                        if coinCheck == False:
                            await event.message.respond(f"{coin} is invalid/does not exist.")
                            return
                await event.message.respond("Coins added. Use !tlist to see watchlist.")
            elif event.content[3:6] == 'del':
                coinToDel = event.content[7:]
                if coinToDel == "":
                    await event.message.respond("No coins given") 
                    return
                priorityCoins.remove(coinToDel.upper())
                await event.message.respond(f"{coinToDel.upper()} deleted successfully!")     
                print(priorityCoins) 
            elif event.content[2:6] == 'list':
                embed = hikari.Embed(title="Coins on watchlist", description='Use !t to get prices on all the coins at once', color="#FF0000")
                for coin, details in priorityCoins.items():
                    on_coinbase = details.get('coinbase', False)
                    status = "Watching on Coinbase" if on_coinbase else ""
                    embed.add_field(name=f"{coin} ‣ {status}", value="-")
                await event.message.respond(embed=embed)

        
    if event.content and event.content.startswith("t") and event.content[1] == " ":
        message = (event.content[2:]).upper()
        coins = message.split(" ")
        response = ""
        print(coins)
        for coin in coins:
            price = coinbaseFetcher(coin)
            if price != False:
                response += f"**{coin}**: ${price}\n"
            else:
                price = coinFetcher(coin)
                if price != False:
                    response += f"**{coin}**: ${price}\n"
                else:
                    response += f"**{coin}**: Can't find coin on coinbase or coinapi"
        await event.message.respond(response)
    
    if event.content and event.content.startswith("p") and event.content[1] == " ":
        message = (event.content[2:]).upper()
        stocks = message.split()
        for stock in stocks:
            embed = stockFetcher(stock, event.message)
            await event.message.respond(embed=embed)

    if event.content and event.content.startswith("pa") and event.content[2] == " ":
        message = (event.content[3:]).upper()
        stocks = message.split()
        for stock in stocks:
            embed = afterHoursFetcher(stock, event.message)
            await event.message.respond(embed=embed)

bot.run()
