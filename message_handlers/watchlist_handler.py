from crypto_fetcher.crypto import priorityCoins, messageCreator, coinChecker
import hikari

async def watchlist_handler(event, content):
    message = event.message
    if len(content) == 0:
        response = "Watchlist: \n"
        coins = list(priorityCoins.keys())
        response = messageCreator(coins, response)
        await message.respond(response)
    elif len(content) > 0:
        action = content[1:len(content)]
        print(action)
        if action.startswith('add'):
            coinsToAdd = content[5:]
            print(coinsToAdd)
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

            await message.respond("Coins added. Use !t list to see watchlist.")

        elif action.startswith('del'):
            coinToDel = content[5:]
            if coinToDel == "":
                await message.respond("No coins given")
                return

            if coinToDel.upper() not in priorityCoins:
                await message.respond(f"{coinToDel.upper()} does not exist in the watchlist.")
                return

            del priorityCoins[coinToDel.upper()]
            await message.respond(f"{coinToDel.upper()} deleted successfully!")
            print(priorityCoins)

        elif action == 'list':
            embed = hikari.Embed(title="Coins on watchlist", description='Use !t to get prices on all the coins at once', color="#FF0000")
            for coin, details in priorityCoins.items():
                embed.add_field(name=f"{coin}", value="-")
            await message.respond(embed=embed)