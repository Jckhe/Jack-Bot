from stock_fetcher.stocks import stockFetcher

async def stock_handler(event, content):
  stocks = content.split()
  message = event.message
  for stock in stocks:
    embed = stockFetcher(stock, event.message)
    await message.respond(embed=embed)