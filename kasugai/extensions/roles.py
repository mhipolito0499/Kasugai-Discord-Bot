import hikari as h
import lightbulb as lb
import miru as m
from kasugai.bot import bot

class RoleButton(m.Button):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


roles_plugin = lb.Plugin("add_roles_plugin")
roles_button_listener = lb.Plugin("roles_button_listener")

@roles_plugin.command
@lb.command("roles", "assign or remove yourself to roles")
@lb.implements(lb.SlashCommand)
async def roles(ctx):
    roles_for_buttons = []
    role_ids = []
    guild = ctx.member.get_guild()
    roles = await guild.fetch_roles()
    for i in roles:
        if i.name != '@everyone' and i.bot_id == None:
            roles_for_buttons.append(i.name)
            role_ids.append(i.id)
    view = m.View()
    for x in range(len(roles_for_buttons)):
        view.add_item(RoleButton(style=h.ButtonStyle.PRIMARY, label=roles_for_buttons[x], custom_id=str(role_ids[x])))
        
    message = await ctx.respond("Choose roles for notifications!", components=view.build())
    view.start(await message.message())

    await view.wait()



@roles_button_listener.listener(m.ComponentInteractionCreateEvent)
async def listen_for_roles(event: m.ComponentInteractionCreateEvent):
    my_roles = []
    if not isinstance(event.interaction, m.ComponentInteraction):
        return
    else:
        member_roles = event.context.member.get_roles()
        for y in member_roles:
            if y.id != event.context.guild_id:
                my_roles.append(str(y.id))
        if event.context.interaction.custom_id in my_roles:
            await event.context.app.rest.remove_role_from_member(event.context.guild_id, event.context.member.id, int(event.context.interaction.custom_id))
        else:
            await event.context.app.rest.add_role_to_member(event.context.guild_id, event.context.member.id, int(event.context.interaction.custom_id))
    
        
            
    
            

    


def load(bot):
    bot.add_plugin(roles_plugin)
    bot.add_plugin(roles_button_listener)

def unload(bot):
    bot.remove_plugin(roles_plugin)
    bot.remove_plugin(roles_button_listener)
    