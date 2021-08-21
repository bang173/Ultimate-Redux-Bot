import discord
from discord import __version__ as discord_version
import os
from discord.ext import commands
from psutil import Process, virtual_memory
import datetime





client = commands.Bot(command_prefix = commands.when_mentioned_or('r!'), intents=discord.Intents.all())



def isitme(ctx):
    return ctx.author.id == 0 or ctx.author.id == 1

def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner_id

client.remove_command('help')

@client.event
async def on_ready():
    print('bot run. \n \n what Logs?:')


@client.event
async def on_guild_join(guild: discord.Guild):
    print(f'joined to guild "{guild.name}"')

@client.event
async def on_guild_remove(guild: discord.Guild):
    print(f'removed from guild "{guild.name}"')
    
    
@client.command(aliases = ['stats', 'стат', 'стата', 'статистика'])
async def stat(ctx):
    try:
        embed = discord.Embed(
            title = 'Статистика бота',
            color = ctx.author.color,
            timestamp = datetime.datetime.now()
        )
        embed.set_thumbnail(url=client.user.avatar.url)
        proc = Process()
        with proc.oneshot():
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            ('discord.py - версия', discord_version, True),
            ('Использование памяти', f'{mem_usage:,.0f} МБ / {mem_total/1000:.3f} ГБ ({mem_of_total:.0f}%)', True),
            ('Пинг', f'`{round(client.latency*1000)}` ms', True)
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)



@client.command()
@commands.check(isitme)
async def load(ctx, extension):
    client.load_extension(f'extra.{extension}')
    await ctx.send(f'{extension} loaded.')
    print(f'{extension} loaded.')

@client.command()
@commands.check(isitme)
async def unload(ctx, extension):
    client.unload_extension(f'extra.{extension}')
    await ctx.send(f'{extension} unloaded.')
    print(f'{extension} unloaded.')

@client.command()
@commands.check(isitme)
async def extensions(ctx):
    await ctx.send(', '.join([ex for ex in client.extensions]))

for filename in os.listdir('./extra'):
    if filename.endswith('.py'):
        client.load_extension(f'extra.{filename[:-3]}')
        print(f'{filename} loaded')






with open('token.txt', 'r') as f:
    token = f.read()
client.run(token)
