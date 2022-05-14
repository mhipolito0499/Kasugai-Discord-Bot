import attr
import lightbulb as lb
import datetime

from hikari.traits import RESTAware
from hikari.events.base_events import Event
from hikari.users import User
from lightbulb.ext import tasks
from kasugai.bot import bot



on_completion_plugin = lb.Plugin('on_completion_plugin')
on_successful_register_plugin = lb.Plugin('on_successful_register_plugin')




@attr.define()
class SuccessfulRegisterEvent(Event):

    app: RESTAware = attr.field()

    author: User = attr.field()
    '''The user who registered the assignment'''

    content: str = attr.field()
    '''The message, should print successful register message from register command'''

    time_created: datetime.datetime = attr.field()
    '''Date/Time assignment was successfully registered'''

    loop_execution: int = attr.field()
    '''Number of times to send reminder'''


@on_completion_plugin.listener(lb.SlashCommandCompletionEvent)
async def on_completion(event: lb.SlashCommandCompletionEvent) -> Event:
    try:
        register_response = await event.context.previous_response.message()
    except AttributeError:
        pass
    else:
        if register_response.content == f'Noted, {event.context.options.assignment} is due on {event.context.options.duedate} for {event.context.options.section}':
            set_dm_message = f'Remember, {event.context.options.assignment} is due on {event.context.options.duedate} {event.context.options.time} for {event.context.options.section}!'
            due_date = datetime.datetime.strptime(event.context.options.duedate, '%m/%d/%Y')
            date_registered = datetime.datetime.now()
            loop_days = due_date - date_registered
            event = SuccessfulRegisterEvent(
                app=bot,
                author= event.context.author,
                content=set_dm_message,
                time_created= date_registered,
                loop_execution= loop_days.days + 1,
                
            )
            bot.dispatch(event)
        else:
            pass




@on_successful_register_plugin.listener(SuccessfulRegisterEvent)
async def on_successful_register(event: SuccessfulRegisterEvent):
    @tasks.task(s=5, max_executions=event.loop_execution)
    async def loop_message():
        await event.author.send(event.content)
    loop_message.start()
    

def load(bot):
    bot.add_plugin(on_completion_plugin)
    bot.add_plugin(on_successful_register_plugin)

def unload(bot):
    bot.remove_plugin(on_completion_plugin)
    bot.remove_plugin(on_successful_register_plugin)