import re
import requests
import json
import time
import asyncio

_pattern = re.compile(r'(?<!^)(?=[A-Z])')
min_time = 0


def to_snake(name):
    return _pattern.sub('_', name).lower()


seconds_in_a_week = 604800


def configure_max_history(max_age):
    global min_time
    min_time = time.time() - max_age


configure_max_history(seconds_in_a_week)  # only take the last week into account


class TradeElement:
    def __init__(self, s):
        self.crafting_margin = 0
        self.craftable = False
        self.faction = ''
        self.name = "no name"
        self.id = "no id"
        self.buy_orders = 0
        self.sell_offers = 0
        for name, value in s.items():
            setattr(self, to_snake(name), value)
        """
        r = requests.get(f"https://crossoutdb.com/data/item/all/{self.id}")
        detail_data = json.loads(r.text)["Data"]
        self.sell_price_trend = {e[0]: e[1] for e in detail_data[0] if e[0] > min_time and e[1] > 0}
        self.buy_price_trend = {e[0]: e[1] for e in detail_data[1] if e[0] > min_time and e[1] > 0}
        self.average_sell_price = sum(self.sell_price_trend.values()) / len(
            self.sell_price_trend) if self.sell_price_trend else 0
        self.average_buy_price = sum(self.buy_price_trend.values()) / len(
            self.buy_price_trend) if self.buy_price_trend else 0
        self.average_margin = int((
                                      self.average_sell_price * 0.9 - self.average_buy_price if self.average_buy_price * self.average_sell_price else 0) * 100) / 100
        """

    def __str__(self):
        return f"{self.name}, id: {self.id}"

    def get_faction(self):
        return self.faction

    def is_craftable(self):
        return self.craftable and self.faction

    def get_crafting_margin(self):
        return self.crafting_margin

    """
    def get_average_margin(self):
        return self.average_margin

    def get_average_buy_price(self):
        return self.average_buy_price

    def non_zero(self):
        return self.buy_orders > 0 and self.sell_offers > 0 and self.average_buy_price > 0 and self.average_sell_price > 0
    """


r = requests.get("https://crossoutdb.com/data/search")
data = {x["id"]: TradeElement(x) for x in filter(lambda e: not e["removed"], json.loads(r.text)["data"])}


def by_id(id):
    return data[id]


def tax(price):
    return 0.9 * price


def matches_category_id(id):
    return lambda t: t.category_id == id


def by_name(name):
    name = name.lower()
    for e in data.values():
        if name in e.name.lower():
            print(e)


refresh_listeners = []


async def refresh_loop():
    while True:
        await asyncio.sleep(60)
        print("refreshing data")
        data = {x["id"]: TradeElement(x) for x in filter(lambda e: not e["removed"], json.loads(r.text)["data"])}
        call_refresh_liseners()


def register_refresh_listener(l):
    l()
    refresh_listeners.append(l)


def call_refresh_liseners():
    for l in refresh_listeners:
        l()


asyncio.ensure_future(refresh_loop())
