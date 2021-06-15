def prettify_coins(coins):
    pretty_strings = [f"{coin['symbol']}:{coin['price']}" for coin in coins]
    return "\n".join(pretty_strings)