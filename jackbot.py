import hikari
import requests
import os
import lightbulb
from dotenv import load_dotenv
from nft import fetcher
from crypto import coinFetcher
from stocks import stockFetcher
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
    if event.content and event.content.startswith("t"):
        message = (event.content[2:]).upper()
        coins = message.split(" ")
        response = ""
        for coin in coins:
            price = coinFetcher(coin)
            response += f"**{coin}**: ${price}\n"
        await event.message.respond(response)
    
    if event.content and event.content.startswith("p"):
        message = (event.content[2:]).upper()
        stocks = message.split()
        for stock in stocks:
            embed = stockFetcher(stock, event.message)
            await event.message.respond(embed=embed)

bot.run()
