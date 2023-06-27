from dotenv import load_dotenv
import requests
import finnhub
import os
import hikari
load_dotenv(override=False)
finnhub_token = os.environ.get('FINNHUB_TOKEN')
finnhub_client = finnhub.Client(api_key=finnhub_token)

# def stockFetcher(message):
#   price = finnhub_client.quote(message)
#   output = (
#     hikari.Embed(title=f"{message} price", description='', color="#FF0000")
#     .add_field(name="Current Price: ", value=f"${price['c']}", inline=True)
#     .add_field(name="Change", value=price['d'], inline=True)
#     .add_field(name="% Change", value=price['dp'], inline=True)
#     .set_footer(text='yammy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
#     )
#   return output

# async def stockFetcher(stocks, ctx):
#     for stock in stocks:
#         embed = hikari.Embed(title=f"{stock} Price", description='', color="#FF0000")
#         price = finnhub_client.quote(stock)
#         embed.add_field(name="Current Price", value=f"${price['c']}", inline=True)
#         embed.add_field(name="Change", value=price['d'], inline=True)
#         embed.add_field(name="% Change", value=price['dp'], inline=True)
#         embed.set_footer(text='yammy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')

#         await ctx.respond(embed=embed)
def stockFetcher(stock, message):
    embed = hikari.Embed(title=f"{stock} Price", description='', color="#FF0000")
    price = finnhub_client.quote(stock)
    embed.add_field(name="Current Price", value=f"${price['c']}", inline=True)
    embed.add_field(name="Change", value=price.get('d', 'N/A'), inline=True)
    embed.add_field(name="% Change", value=price.get('dp', 'N/A'), inline=True)
    embed.set_footer(text='yammy', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')

    return embed