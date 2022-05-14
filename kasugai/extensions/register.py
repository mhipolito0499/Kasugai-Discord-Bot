import os
import datetime
import hikari as h
import lightbulb as lb
import psycopg2


from psycopg2 import *


register_plugin = lb.Plugin("register_plugin")
register_completion_plugin = lb.Plugin("register_completion_plugin")
on_successful_registration_plugin = lb.Plugin("on_successful_registration_plugin")


conn = psycopg2.connect(
    host=os.environ["HOST_NAME"],
    database=os.environ["DATABASE_NAME"],
    user=os.environ["PRIMARY_USER"],
    password=os.environ["PASSWORD"],
    port= int(os.environ["PORT_KEY"])
)

cursor = conn.cursor()
conn.autocommit = True

@register_plugin.command
@lb.option('time', 'Time assignment is due **FORMAT: H:M AM/PM (example: 11:59 PM)')
@lb.option('duedate', 'Date and time assignment is due. **FORMAT: MM/DD/YYYY (example: 03/24/2022)**')
@lb.option('assignment', 'Assignment name')
@lb.option('section', 'Class assignment is from. Format: @"class" (example: @comp380)', type=h.Role)
@lb.command('register', 'Set up a notification for an upcoming assignment.', aliases=["register"], ephemeral=True)
@lb.implements(lb.SlashCommand,lb.PrefixCommand)
async def register(ctx):
    duedate = ctx.options.duedate
    time_due = ctx.options.time
    assignment = ctx.options.assignment
    section = ctx.options.section
    guildID = ctx.member.guild_id
    userID = ctx.member.id
    username = ctx.member.username
    ######checks for proper input before sending it to database:###########
    class_id = section.id
    class_name = section.name
    role_ids = ctx.member.role_ids
    date_format = '%m/%d/%Y'


    #checks if user has assigned role and disallows the user to use @everyone role
    if class_id not in role_ids:
        await ctx.respond('You are not assigned to this class! Check if you are assigned to the class and try the command again.')
    elif class_id == guildID:
        await ctx.respond('This role is not a valid class!')
    else:
        try:
            datetime.datetime.strptime(ctx.options.duedate, date_format)
        except ValueError:
            await ctx.respond('Invalid Date format! **FORMAT: MM/DD/YYYY (example: 03/25/2022)**')
        else:
            #store user input into database
            query = "INSERT INTO student (guild_id, user_id, username, section, section_id, assignment, due_date, time) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            data = (guildID, userID, username, class_name, class_id, assignment, duedate, time_due)
            #check for invalid dates
            try: 
                cursor.execute(query, data)
            except psycopg2.errors.InvalidDatetimeFormat:
                await ctx.respond(f'Invalid date or time format!')
            else:
                #commit user input to database
                conn.commit()
                await ctx.respond(f'Noted, {ctx.options.assignment} is due on {ctx.options.duedate} for {ctx.options.section}')


def load(bot):
    bot.add_plugin(register_plugin)

def unload(bot):
    bot.remove_plugin(register_plugin)
    
