import nextcord
from nextcord import File, ButtonStyle
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord.utils import get
import dotenv
import aiosqlite
import datetime
import os
from os import environ as env
import wavelink

dotenv.load_dotenv()

intents=nextcord.Intents.all()

prefix = '$'
bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Бот готов к использованию')



@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Привет, {member.name}, добро пожаловать на наш сервер!\nОбязательно ознакомься с информацией в приветственном канале.')

@bot.command(name='hello')
async def msg(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send("Sup!")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Похоже, вы пропустили аргумент для этой команды.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Похоже, у вас нет прав на выполнение этой команды.")
    if isinstance(error, commands.MissingRole):
        await context.send("Похоже, у вас нет ролей для этой команды.")
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Похоже, у меня нет прав для этой команды.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Похоже, у меня нет ролей для этой команды.")
 
@bot.command()
async def help(message):
    helpC = nextcord.Embed(title="moderator Bot \nHelp Guide", description="Дискорд бот для модерации")
    helpC.add_field(name="Clear", value="Чтобы использовать эту команду, введите \"$clear\" и количество сообщений, которые вы хотите удалить, по умолчанию это 5.", inline=False)
    helpC.add_field(name="kick/ban/unban", value="Чтобы использовать эту команду, введите $kick/$ban/$unban, затем укажите пользователя, на которого вы хотите выполнить эту команду, ВНИМАНИЕ: пользователь должен иметь права для использования этой команды.", inline=False)

    await message.channel.send(embed=helpC)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)


@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : nextcord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'{member} кикнули')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : nextcord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} забанен')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} разбанен')
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : nextcord.Member, days, reason=None):
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} ненадолго забанен')
    await asyncio.sleep(days)
    print("It's unban time!")
    await member.unban()
    await context.send(f'{member} разбанен')


bot.run(env['TOKEN'])