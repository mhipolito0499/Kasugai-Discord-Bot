import os
import hikari as h
import lightbulb as lb
import psycopg2
import datetime
from datetime import *
from psycopg2 import *

whats_due_plugin = lb.Plugin("whats_due_plugin")

conn = psycopg2.connect(
    host=os.environ["HOST_NAME"],
    database=os.environ["DATABASE_NAME"],
    user=os.environ["PRIMARY_USER"],
    password=os.environ["PASSWORD"],
    port= int(os.environ["PORT_KEY"])
)

cursor = conn.cursor()
conn.autocommit = True



@whats_due_plugin.command
@lb.command("whatsdue", "A list of your assignments that's due", ephemeral=True)
@lb.implements(lb.SlashCommand, lb.PrefixCommand)
async def whatsdue(ctx):
    t=(f'{ctx.member.guild_id}',f'{ctx.member.id}',)
    cursor.execute("SELECT assignment, section, due_date, time FROM student WHERE (guild_id = %s AND user_id = %s)", t)
    homework_due = cursor.fetchall()
    embed = h.Embed(title="Assignments due",color="#44EA55")
    for x in homework_due:
        due_date = x[2].strftime('%m/%d/%Y')
        embed.add_field(name=str(x[0]),value=f"Class: {x[1]}\nDue Date: {due_date}\nTime: {x[3].strftime('%I:%M %p')}")
    await ctx.author.send(embed)
    await ctx.respond("Check DM's for assignments due!")
    



def load(bot):
    bot.add_plugin(whats_due_plugin)

def unload(bot):
    bot.remove_plugin(whats_due_plugin)