import hikari
import requests
import os
from dotenv import load_dotenv
from nft import fetcher
from crypto import coinFetcher, priorityCoins, coinbaseFetcher
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
        print(event.content)
        if len(event.content) > 2:
            print(event.content[3:6])
            if event.content[3:6] == 'add':
                coinToAdd = event.content[7:]
                if coinToAdd == "":
                    await event.message.respond("No coins given") 
                    return
                priorityCoins.append(coinToAdd.upper())
                await event.message.respond(f"{coinToAdd.upper()} added successfully!") 
                print(priorityCoins)
            elif event.content[3:6] == 'del':
                coinToDel = event.content[7:]
                if coinToDel == "":
                    await event.message.respond("No coins given") 
                    return
                priorityCoins.remove(coinToDel.upper())
                await event.message.respond(f"{coinToDel.upper()} deleted successfully!")     
                print(priorityCoins) 
        else:
            response = "List of coins watching on coinbase: \n"
            for coin in priorityCoins:
                response += f" ‣ ***{coin}***\n"
            print(response)
            await event.message.respond(response)    

        
    if event.content and event.content.startswith("t") and event.content[1] == " ":
        message = (event.content[2:]).upper()
        coins = message.split(" ")
        response = ""
        print(coins)
        for coin in coins:
            if coin in priorityCoins:
                price = coinbaseFetcher(coin)
                response += f"**{coin}** (cb): ${price}\n"
            else:
                price = coinFetcher(coin)
                response += f"**{coin}**: ${price}\n"
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
