import hikari
import requests
import os
from dotenv import load_dotenv
#NFT Imports
from nft import fetcher
#Cryptocurrency Imports
from crypto_fetcher.crypto import coinFetcher, priorityCoins, coinbaseFetcher, coinChecker, messageCreator
from message_handlers.watchlist_handler import watchlist_handler
from message_handlers.crypto_handler import crypto_handler
#Stocks Imports
from stock_fetcher.stocks import stockFetcher, afterHoursFetcher
from message_handlers.stock_handler import stock_handler

load_dotenv(override=False)
discord_token = os.environ.get('TOKEN')
admin_token=os.environ.get('ADMIN')


#intent
bot = hikari.GatewayBot(
    discord_token,
    intents=hikari.Intents.ALL_UNPRIVILEGED  # Add this
    | hikari.Intents.MESSAGE_CONTENT,        # 
)

#PREFIXES for message commands/creation
WATCHLIST_PREFIX = "!t"
CRYPTO_PREFIX = "t "
STOCK_PREFIX = "p "


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    content = event.content
    message = event.message

    if content and content.startswith(WATCHLIST_PREFIX):
        await watchlist_handler(event, content[2:])
      
    if content and content.startswith(CRYPTO_PREFIX):
        await crypto_handler(event, (content[2:]).upper())
    
    if content and content.startswith(STOCK_PREFIX):
        await stock_handler(event, (content[2:]).upper())

bot.run()
