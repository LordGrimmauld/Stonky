import tradeelement

factions = None


def refresh_factions():
    global factions
    factions = {*filter(None, map(tradeelement.TradeElement.get_faction, tradeelement.data.values()))}


tradeelement.register_refresh_listener(refresh_factions)
