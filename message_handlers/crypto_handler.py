from crypto_fetcher.crypto import messageCreator

async def crypto_handler(event, content):
  message = event.message
  coins = content.split(" ")
  response = ""
  print(coins)
  response = messageCreator(coins, response)
  await message.respond(response)
