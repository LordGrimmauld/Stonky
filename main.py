import os
import subprocess
import discord
import json
import sys
from discord.ext import commands


def read_config():
    with open("config.json", "r") as f:
        c = json.load(f)
        return c.get("token", None), \
               c.get("invite",
                     "https://discord.com/api/oauth2/authorize?client_id=901089315751350392&permissions=311385214016&scope=applications.commands%20bot"), \
               c.get("owner", 533668542562828311), \
               c.get("github", "https://github.com/LordGrimmauld/Stonky")


if __name__ == "__main__":
    token, invite, owner, github = read_config()
    if token is None:
        sys.exit()

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


    @bot.command("invite")
    async def _invite(ctx):
        embed = discord.embeds.Embed(title=invite)
        await ctx.send(embed=embed)


    @bot.command("github")
    async def _github(ctx):
        embed = discord.embeds.Embed(title=github)
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await ctx.send(embed=embed)


    @bot.command("update")
    async def _update(ctx):
        output = subprocess.check_output(["git", "pull"]).decode("utf-8").strip()
        embed = discord.Embed(title="Updating bot...", url=github,
                              description=output)
        await ctx.send(embed=embed)
        if output != "Already up to date." or True:
            os.execv(sys.executable, ['python'] + sys.argv)
            sys.exit()


    @bot.command("stop")
    async def _stop(ctx):
        await bot.close()

    print("starting bot...")
    bot.run(token)
