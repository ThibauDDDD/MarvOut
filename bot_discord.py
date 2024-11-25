#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive
from get_push_github import get_list_commit, check_list_commit, check_new_push


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
list_of_repo = {}

# @bot.command()
# async def bonjour(ctx):
#     if (ctx.author.nick):
#         await ctx.send(f"Bonjour {ctx.author.nick} !")
#     else:
#         await ctx.send(f"Bonjour {ctx.author.global_name} !")

# @bot.command()
# async def ping(ctx):
#     await ctx.send("Pong!")


async def async_loop_check_new_push(github_token: str, owner: str, repo: str, channel: discord.TextChannel): # Boucle pour vérifier périodiquement les nouveaux pushs
    """cette fonction est une boucle permettant de vérifier toutes les 60 secondes si quelqu'un a push sur le repo indiqué  en argument

    Args:
        github_token (str): Un discord token. Trouvable sur son compte github. Sinon, tapez github token dans google et ça vous enverra sur le bon lien github
        owner (str): Le pseudo Github du propriétaire du repository github
        repo (str): Le nom du repository Github
        channel (discord.TextChannel): Le salon dans lequel vous voulez que les notifications soient postées.
    """
    last_push_id = [""] # identifiant du dernier push détecté.
    while (list_of_repo.get(repo) != None):
        is_new_push = check_new_push(repo, get_list_commit(github_token, owner, repo), last_push_id)
        if (is_new_push != False):
            print(is_new_push)
            await channel.send(is_new_push)
        elif (is_new_push == False):
            print("pas de nouveau push")
        else:
            return()
        await asyncio.sleep(10)# Vérifie toutes les 60 secondes



@bot.tree.command()
async def define(interaction: discord.Interaction, channel: discord.TextChannel, github_token: str, owner: str, repository: str):
    """Envoie un message quand quelqu'un a push sur le repository

    Args:
        interaction (discord.Interaction): l'argument de base des bot.tree.command
        channel (discord.TextChannel): Le salon dans lequel vous voulez que les notifications soient postées.
        github_token (str): Votre github token.
        owner (str): Le pseudo Github du propriétaire du repository github
        repository (str): Le nom du repository Github
    """
    check_error = check_list_commit(get_list_commit(github_token, owner, repository))

    if (check_error != True):
        if (check_error[0] == 401):
            print(check_error[1])
            await interaction.response.send_message(f"votre token github n'est pas correct, veuillez réessayer s'il vous plaît")
        elif (check_error[0] == 404):
            await interaction.response.send_message(f"le nom du du repository et / ou du propriétaire du repository n'est pas correct, veuillez réessayer s'il vous plaît")
        else:
            await interaction.response.send_message("il y a eu une erreur")
    if (list_of_repo.get(repository) != None):
            await interaction.response.send_message(f"ce repository est déjà vérifié dans le salon {list_of_repo.get(repository)}")
    if (check_error == True):
        list_of_repo[repository] = channel.name
        await interaction.response.send_message(f"merci, les notifications de push seront envoyés dans le channel {channel}")
        asyncio.create_task(async_loop_check_new_push(github_token, owner, repository, channel))

@bot.tree.command()
async def stop(interaction: discord.Interaction, repository: str):
    """arrête de vérifier le repository

    Args:
        interaction (discord.Interaction): l'argument de base des bot.tree.command
        repository (str): Le nom du repository Github
    """
    if (list_of_repo.get(repository) == None):
            await interaction.response.send_message(f"ce repository n'est pas vérifié")
            return
    del list_of_repo[repository]
    await interaction.response.send_message(f"{repository} ne sera plus vérifié")



@bot.event
async def on_ready():
    print(f"ici {bot.user}")
    result = await bot.tree.sync() #permet d'ajouter les fonctions avec slash au bot discord
    print(result)

@bot.event
async def on_guild_join(guild:discord.Guild):
    """Se lance quand le bot rejoint un serveur discord

    Args:
        guild (discord.Guild): l'argument de base de on guild join
    """

    # Message à envoyer
    message = (
        f"Bonjour à tous dans le serveur **{guild.name}** ! 🎉\n"
        "Merci de m'avoir ajouté. tapez \"/\" pour voir mes commandes disponibles!"
    )
    # Cherche un canal où le bot peut envoyer un message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(message)
            break
    else:
        print(f"Aucun canal approprié trouvé pour envoyer un message dans {guild.name}.")

def main():
    load_dotenv(dotenv_path=".env") #permet de récupérer le token 
    keep_alive()
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()