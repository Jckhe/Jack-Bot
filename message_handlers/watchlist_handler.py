from crypto_fetcher.crypto import priorityCoins, messageCreator

async def watchlist_handler(event, content):
    message = event.message

    if len(content) == 0:
        response = "Watchlist: \n"
        coins = list(priorityCoins.keys())
        response = messageCreator(coins, response)
        await message.respond(response)
    elif len(content) > 0:
        action = content[:3]
        if action == 'add':
            coinsToAdd = content[4:]

            if not coinsToAdd:
                await message.respond("No coins given")
                return

            coinsToAdd = coinsToAdd.split(" ")

            for coin in coinsToAdd:
                if coin in priorityCoins:
                    await message.respond(f"{coin} already exists.")
                    continue
                else:
                    coinCheck = coinChecker(coin)
                    if coinCheck is False:
                        await message.respond(f"{coin} is invalid/does not exist.")
                        return

            await message.respond("Coins added. Use !tlist to see watchlist.")

        elif action == 'del':
            coinToDel = content[4:]
            if coinToDel == "":
                await message.respond("No coins given")
                return

            if coinToDel.upper() not in priorityCoins:
                await message.respond(f"{coinToDel.upper()} does not exist in the watchlist.")
                return

            priorityCoins.remove(coinToDel.upper())
            await message.respond(f"{coinToDel.upper()} deleted successfully!")
            print(priorityCoins)

        elif action == 'lis':
            embed = hikari.Embed(title="Coins on watchlist", description='Use !t to get prices on all the coins at once', color="#FF0000")
            for coin, details in priorityCoins.items():
                on_coinbase = details.get('coinbase', False)
                status = "Watching on Coinbase" if on_coinbase else ""
                embed.add_field(name=f"{coin} ‣ {status}", value="-")
            await message.respond(embed=embed)