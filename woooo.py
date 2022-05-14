import discord
from discord.ext import commands
import asyncio
import asyncpg
import os
import datetime

intents = discord.Intents().default()
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix="ww.", help_command=None, intents=intents, activity=discord.Activity(
    type=discord.ActivityType.watching, name="Woooooo! Lemme Watch Your Games"))

@client.event
async def on_ready():
    print("Woooooo....\nIm Ready For Some Fun")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return
    raise error

class ViewButton(discord.ui.Button):
    def __init__(self,tur,user):
        User_Avatar = user.avatar
        if tur == "PNG":
            User_Avatar = User_Avatar.with_format("png")
        if tur == "JPG":
            User_Avatar = User_Avatar.with_format("jpg")
        if tur == "WEBP":
            User_Avatar = User_Avatar.with_format("webp")
        if tur == "GIF":
            User_Avatar = User_Avatar.with_format("gif")
        super().__init__(label=f"[{tur}]",style=discord.ButtonStyle.link,url=User_Avatar.url,row=0)

@client.command(name="avatar")
async def avatar(ctx, member = None):
    if member == None:
        member = ctx.author
    else:
        try:
            member = await commands.MemberConverter().convert(ctx,member)
        except:
            await ctx.send("Bu Kullanıcıyı Bulamadım :c")
            return
    View = discord.ui.View()
    View.add_item(ViewButton("PNG",member))
    View.add_item(ViewButton("JPG",member))
    View.add_item(ViewButton("WEBP",member))
    if member.avatar.is_animated():
        View.add_item(ViewButton("GIF",member))
    await ctx.send("Avatar", view=View)

@client.command("line-count")
async def line_count(ctx):
    cogs = list(filter(lambda m: m[-3:] == ".py" or m == "woooo.py", list(os.listdir("./cogs"))))
    cogs.append("woooo.py")
    lines = 0
    classes = 0
    funcs = 0
    async_funcs = 0
    for cog in cogs:
        if cog == "woooo.py":
            with open(f"woooo.py", "r", encoding="UTF-8") as f:
                read = f.read().split("\n")
                lines += len(read)
                for line in read:
                    if "class" in line:
                        classes += 1
                    if "async def" in line:
                        async_funcs += 1
                        continue
                    if "def" in line:
                        funcs += 1
        else:
            with open(f"./cogs/{cog}", "r", encoding="UTF-8") as f:
                read = f.read().split("\n")
                lines += len(read)
                for line in read:
                    if "class" in line:
                        classes += 1
                    if "async def" in line:
                        async_funcs += 1
                        continue
                    if "def" in line:
                        funcs += 1
    await ctx.send(f"Total Files: {len(cogs)}\nTotal Lines: {lines}\nTotal Classes: {classes}\nTotal Functions: {funcs}\nTotal Async Functions: {async_funcs}")


@client.command(name="ping")
async def ping(ctx):
    start = datetime.datetime.now()
    async with client.pool.acquire() as con:
        await con.fetchrow("select version();")
    database_latency = datetime.datetime.now() - start
    await ctx.send(f"DB Gecikmesi : {database_latency.seconds if database_latency.microseconds % 1000 != 0 else database_latency.seconds + 1}.{round(database_latency.microseconds,3) if database_latency.microseconds % 1000 != 0 else 0}\nBot Gecikmesi : {round(client.latency * 1000,3)}")


if __name__ == "__main__":
    client.pool = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(
        user="postgres", password="kutup", database="werewolf", host="127.0.0.1"))
    print("I Got You DATABASE")
    cogs = filter(lambda m: m[-3:] == ".py", os.listdir("./cogs"))
    client.load_extension("jishaku")
    for cog in cogs:
        with open(f"./cogs/{cog}", "r", encoding="UTF-8") as f:
            readed = f.read()
            if "def setup(client):" not in readed:
                continue
        client.load_extension("cogs." + cog[:-3])
        print(cog[0].upper() + cog[1:-3], "Loaded Succesfully!")

client.run("ODQ1NjU5Mzg1OTgwMjU2Mjc2.YKkLrQ.vzDOwMfSkbPjgINHd4PAQqbqoYY")
