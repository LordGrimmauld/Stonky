import tradeelement
import discord

crafts = {}
colors = {"Rare": [0, 102, 204], "Special": [51, 202, 204], "Epic": [185, 0, 255], "Legendary": [255, 158, 64]}


def update_crafts():
    for part in filter(tradeelement.TradeElement.is_craftable, tradeelement.data.values()):
        if part.rarity_id == 1 or part.rarity_id == 5:
            continue
        if part.rarity_name not in crafts.keys():
            crafts[part.rarity_name] = {}
        if part.faction not in crafts[part.rarity_name].keys():
            crafts[part.rarity_name][part.faction] = []
        crafts[part.rarity_name][part.faction].append(part)
    for rarity, factions in crafts.items():
        for faction, parts in factions.items():
            crafts[rarity][faction] = sorted(crafts[rarity][faction], key=tradeelement.TradeElement.get_crafting_margin,
                                             reverse=True)[:5]


tradeelement.register_refresh_listener(update_crafts)


def convert(r, g, b):
    return (r << 16) + (g << 8) + b


def generate_embeds():
    for rarity, factions in crafts.items():
        embed = discord.Embed(title=f"crafting {rarity} parts",
                              url=f"https://crossoutdb.com/#preset=crafting.rarity={rarity.lower()}.craftable=true",
                              color=convert(*(colors.get(rarity, [0, 0, 0]))))
        for faction, parts in factions.items():
            embed.add_field(name=faction, value="\n".join(f"{part.name}: {part.format_margin}" for part in parts),
                            inline=True)
        yield embed
