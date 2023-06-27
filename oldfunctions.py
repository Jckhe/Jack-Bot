# def coinFetcher(coin):
#     headers = {'X-CoinAPI-Key' : coin_token}
#     coin = requests.request("GET", f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD", headers=headers)
#     coin = coin.json()
#     return round(coin['rate'], 2)

# def fetcher(slug):
#     """Fetch data from OpenSea API."""
#     fetch_url = f"https://api.opensea.io/api/v1/collection/{slug}/stats"
#     headers = {"Accept": "application/json"}
#     response = requests.get(fetch_url, headers=headers)
#     data = response.json()

#     # Extract and process data from the JSON response
#     stats = data['stats']
#     floor_price = round(stats['floor_price'], 3)
#     one_day_volume = round(stats['one_day_volume'], 1)
#     seven_day_volume = round(stats['seven_day_volume'], 1)
#     total_volume = round(stats['total_volume'], 1)
#     supply = int(stats['total_supply'])
#     holders = stats['num_owners']
#     holder_ratio = round(supply / holders, 2)

#     # Fetch additional data
#     os_url = f"https://opensea.io/collection/{slug}"
#     os_thumbnail = image_fetcher(slug)
#     os_title = title_fetcher(slug)
#     royalty = royalty_fetcher(slug)

#     # Create embed for the data
#     embed = hikari.Embed(title=os_title, description='Click Above For Opensea', url=os_url, color="#FF0000")
#     embed.add_field(name='Total Volume:', value=f"{total_volume} ETH", inline=True)
#     embed.add_field(name='Total Supply:', value=supply, inline=True)
#     embed.add_field(name='Number of Holders:', value=holders, inline=True)
#     embed.add_field(name='Holder Ratio:', value=holder_ratio, inline=True)
#     embed.add_field(name='Royalty Fee', value=royalty, inline=True)
#     embed.add_field(name='**Floor Price**:', value=f"**{floor_price} ETH**")
#     embed.set_footer(text='coded by Ky#0801', icon='https://cdn-icons-png.flaticon.com/512/6699/6699255.png')
#     embed.set_thumbnail(os_thumbnail)

#     return embed
