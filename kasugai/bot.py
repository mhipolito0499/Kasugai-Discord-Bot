import os
import lightbulb as lb
import miru
from lightbulb.ext import tasks


bot = lb.BotApp(
    os.environ["TOKEN"],
    prefix="!",
    #default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True,
)

miru.load(bot)

bot.load_extensions_from('kasugai/extensions')

tasks.load(bot)



def run() -> None:
    bot.run()