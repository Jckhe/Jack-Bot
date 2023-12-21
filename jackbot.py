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
