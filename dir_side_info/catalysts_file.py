import discord
from pymarketcap import Pymarketcap
import datetime
from random import randint
import requests


class Class_Catalysts:
    def __init__(self, auth):
        self.auth = str(auth).split("#")
        self.auth = self.auth[0]
        self.time = datetime.datetime.now().timestamp()
        self.color = randint(0, 0xffffff)
        self.cmcal_default = "https://coinmarketcal.com/api/events?page=1&max=5&showPastEvent=false"
        self.empty_name = ""
        return

    def function_cmc(self, coin):
        if coin == "":
            full_name = self.empty_name
        else:
            coin = coin.upper()
            coinmarketcap = Pymarketcap()
            cmc_json = coinmarketcap.ticker(coin)
            ticker = cmc_json["symbol"]
            name = cmc_json["name"]
            full_name = name + "%20" + "(" + ticker + ")"
        return full_name

    def function_cmcal(self, full_name, event_type):
        event_type = event_type.capitalize()
        if event_type == "" and full_name == "":
            cmcal_url = self.cmcal_default
        elif full_name == "":
            cmcal_url = "https://coinmarketcal.com/api/events?page=1&max=5&categories={}&showPastEvent=false".format(
                event_type)
        elif event_type == "":
            cmcal_url = "https://coinmarketcal.com/api/events?page=1&max=5&coins={}&showPastEvent=false".format(
                full_name)
        else:
            cmcal_url = "https://coinmarketcal.com/api/events?page=1&max=5&coins={}&categories={}&showPastEvent=false".format(
                full_name, event_type)

        r = requests.get(cmcal_url)
        data_json = r.json()
        event = ""
        for i in data_json:
            title = str(i["title"])
            coin_name = str(i["coins"][0]["symbol"])
            date_event = str(i["date_event"])
            date = date_event.split("T")
            date = date[0]
            desc = str(i["description"])
            cat = str(i["categories"])
            cat = cat.split("['")
            cat = cat[1].split("']")
            cat = cat[0]
            event += "[" + coin_name + "]" + " [" + date + "]" + " " + "[" + cat + "]" + "\n[" + title + "] \n" + desc + "\n\n"
        return event

    def function_display(self, event):
        events = "```css\n" + event + "```"
        embed = discord.Embed(colour=discord.Colour(self.color), url="https://discordapp.com",
                              timestamp=datetime.datetime.utcfromtimestamp(self.time))
        embed.add_field(name=":floppy_disk: Information about the incoming events", value=events, inline=True)
        embed.add_field(name="Data retrieved with :heart: from : ", value="```py\nCoinmarketcal.com\n```", inline=False)
        embed.set_footer(text="Request achieved :")
        return embed

    def get_catalysts(self, coin, event_type):
        get_coin = self.function_cmc(coin)
        event = self.function_cmcal(get_coin, event_type)
        embed = self.function_display(event)

        return embed
