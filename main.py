import discord
from discord.ext import commands
import json
import os
import platform
from dotenv import load_dotenv
from os.path import join, dirname

from bcolors import BashColors, colored_print
from channel import Channel

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
written_messages_channel = []
not_written_messages_channel_by_error = []
not_written_messages_channel_by_no_content = []


class MessageSenderBot:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open("./config.json", encoding="utf8") as config_json:
            return json.load(config_json)

    def clear_console(self):
        operating_system = platform.system()
        if operating_system == "Linux" or operating_system == "Darwin":
            os.system("clear")
        elif operating_system == "Windows":
            os.system("cls")

    async def on_ready(self):
        self.clear_console()
        colored_print(f"Bot logado como: {bot.user.name}", BashColors.OKGREEN)

        for message_config in self.config:
            if "message_id" not in message_config:
                colored_print(
                    "Erro:\nTodas as mensagens precisam conter um ID.",
                    BashColors.FAIL,
                    end_spaces=1,
                )
                colored_print("Nenhuma ação foi tomada.", BashColors.OKBLUE)
                os._exit(0)

    async def send_message(self, ctx, message_config):
        title = message_config.get("title", None)
        message_id = message_config.get("message_id", None)
        embed_description = message_config.get("embed_description", None)
        bot_will_purge_channel = message_config.get("purge", False)
        description = message_config.get("description")
        thumbnail_url = message_config.get("thumbnail")
        image_url = message_config.get("image")
        channel_id = int(message_config["channel_id"])
        channel = ctx.guild.get_channel(channel_id)
        written_msg = Channel(
            channel_name=channel.name, message_id=message_config["message_id"]
        )

        if not channel:
            colored_print(
                f"Canal com ID {channel_id} não encontrado.", BashColors.WARNING
            )
            return

        if bot_will_purge_channel:
            colored_print(
                f"* Mensagens do canal {channel.name} apagadas!",
                BashColors.WARNING,
                end_spaces=3,
            )
            await channel.purge()

        try:
            if (
                not description
                and not embed_description
                and not thumbnail_url
                and not image_url
            ):
                not_written_messages_channel_by_no_content.append(written_msg)
                return
            if description:
                await channel.send(description)

            if embed_description:
                if title:
                    embed = discord.Embed(title=title, description=embed_description)
                else:
                    embed = discord.Embed(description=embed_description)
                if thumbnail_url:
                    embed.set_thumbnail(url=thumbnail_url)
                if image_url:
                    embed.set_image(url=image_url)
                await channel.send(embed=embed)
            written_messages_channel.append(written_msg)
            return
        except Exception as error:
            print(
                f'Erro ao enviar message: {message_config["message_id"]} ao canal {channel.name}'
            )
            not_written_messages_channel_by_error.append(written_msg)
            return

    def run(self):
        @bot.event
        async def on_ready():
            await self.on_ready()

        @bot.command(name="enviarmsg")
        async def send_msg(ctx):
            for message_config in self.config:
                channel_id = int(message_config["channel_id"])
                channel = ctx.guild.get_channel(channel_id)
                print(message_config)
                try:
                    await self.send_message(ctx, message_config)

                except Exception as e:
                    print(message_config)
                    colored_print(
                        f"Erro ao enviar mensagem:\n {str(e)}",
                        BashColors.FAIL,
                        end_spaces=2,
                        separator=True,
                    )

            # Restante do código para exibir mensagens escritas e não escritas
            # ...
            colored_print(
                f"Mensagens enviadas:",
                BashColors.OKGREEN,
                separator=True,
            )
            for msg in written_messages_channel:
                print(f"- Mensagem #{msg.message_id} no canal {msg.channel_name}")

            colored_print(
                f"Mensagens não enviadas por erro:",
                BashColors.OKGREEN,
                start_spaces=2,
                separator=True,
            )
            for msg in not_written_messages_channel_by_error:
                print(f"- Mensagem #{msg.message_id} no canal {msg.channel_name}")

            colored_print(
                f"Mensagens não enviadas por falta de conteúdo:",
                BashColors.OKGREEN,
                start_spaces=2,
                separator=True,
            )
            for msg in not_written_messages_channel_by_no_content:
                print(f"- Mensagem #{msg.message_id} no canal {msg.channel_name}")

        bot.run(BOT_TOKEN)


if __name__ == "__main__":
    message_sender = MessageSenderBot()
    message_sender.run()
