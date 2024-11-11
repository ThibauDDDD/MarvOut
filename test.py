#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def bonjour(ctx):
    if (ctx.author.nick):
        await ctx.send(f"Bonjour {ctx.author.nick} !")
    else:
        await ctx.send(f"Bonjour {ctx.author.global_name} !")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

load_dotenv(dotenv_path=".env")

bot.run(os.getenv("TOKEN"))
