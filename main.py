# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
import os
import platform
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
config_json = open("./config.json", encoding="utf8")
config = json.load(config_json)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    NORMAL = "\033[97m"
    WARNING = "\033[33m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


@bot.event
async def on_ready():
    operatin_system = platform.system()
    if operatin_system == "Linux" or operatin_system == "Darwin":
        os.system("clear")
    elif operatin_system == "Windows":
        os.system("cls")
    else:
        pass

    print(f"{bcolors.OKGREEN}Bot logado como: {bot.user.name} {bcolors.RESET}")

    for i in config:
        message_id = i.get("message_id", None)
        if not message_id:
            print(
                f"{bcolors.FAIL}Todas as mensagens precisam conter um ID{bcolors.RESET}."
            )
            print(f"{bcolors.OKBLUE}\n\nNenhuma ação foi tomada.{bcolors.RESET}")
            os._exit(0)


@bot.command(name="enviarmsg")
async def send_msg(ctx):
    written_messages_channel = []
    not_written_messages_channel_by_error = []
    not_written_messages_channel_by_no_content = []

    for i in config:
        title = i["title"]
        message_id = i.get("message_id", None)
        embed_description = i.get("embed_description", None)
        bot_will_purge_channel = i.get("purge", False)
        description = i.get("description", None)

        thumbnail_url = i.get("thumbnail", None)
        image_url = i.get("image", None)

        channel_id = int(i["channel_id"])
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            try:
                if bot_will_purge_channel:
                    print(
                        f"{bcolors.WARNING} * Mensagens do canal {bcolors.UNDERLINE}{channel.name}{bcolors.RESET} {bcolors.WARNING}apagadas!{bcolors.RESET}"
                    )
                    await channel.purge()
                    print("\n\n\n")
                    print("==========================================")
                if description:
                    await channel.send(description)
                    if channel.name not in written_messages_channel:
                        written_messages_channel.append(channel.name)

                if embed_description:
                    embed = discord.Embed(
                        title=title,
                        description=embed_description,
                    )
                    if thumbnail_url:
                        embed.set_thumbnail(url=thumbnail_url)
                    if image_url:
                        embed.set_image(url=image_url)

                    await channel.send(embed=embed)

                    if channel.name not in written_messages_channel:
                        written_messages_channel.append(channel.name)
                if (
                    not embed_description
                    and not description
                    and not thumbnail_url
                    and not image_url
                ):
                    print(
                        f"{bcolors.OKBLUE} Sem conteúdo para enviar, pulando mensagem.{bcolors.RESET}"
                    )
                    not_written_messages_channel_by_no_content.append(channel.name)
                    pass
            except:
                not_written_messages_channel_by_error.append(channel.name)
        else:
            print(
                f"{bcolors.WARNING} Canal com ID {channel_id} não encontrado.{bcolors.RESET}"
            )
    print("\n")
    if len(written_messages_channel) > 0:
        print(f"{bcolors.OKGREEN}Mensagens escritas em:{bcolors.RESET}")
        for channel in written_messages_channel:
            print(f"{bcolors.NORMAL} - {channel}")
    else:
        print(
            f"{bcolors.FAIL}Ops! Parece que não foi possível escrever mensagem a{bcolors.RESET}"
        )
    print("\n")
    if len(not_written_messages_channel_by_error) > 0:
        print(
            f"{bcolors.WARNING}Mensagens não escritas por conta de erro em:{bcolors.RESET}"
        )
        for channel in not_written_messages_channel_by_error:
            print(f"{bcolors.NORMAL} - {channel}")
    print("\n")
    if len(not_written_messages_channel_by_no_content) > 0:
        print(
            f"{bcolors.WARNING}Mensagens não escritas por falta de conteúdo em:{bcolors.RESET}"
        )
        for channel in not_written_messages_channel_by_no_content:
            print(f"{bcolors.NORMAL} - {channel} {bcolors.RESET}")
    config_json.close()


bot.run(BOT_TOKEN)
