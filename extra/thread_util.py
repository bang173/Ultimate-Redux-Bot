import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command
import logging



class ThreadTool(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.ignored = [856558217822994492, 841771697845567488, 812720409082331166, 841771615419105290, 871883550566268958]

    @command()
    @commands.is_owner()
    async def thread_join(self, ctx):
        thread = ctx.guild.threads[0]
        await thread.join()
        await ctx.send('done')
        await thread.send('done')
        

    @command()
    @commands.is_owner()
    async def threads(self, ctx):
        print(ctx.guild.threads)


    @command()
    @commands.is_owner()
    async def retreive_thread_messages(self, ctx):
        await ctx.send('started process')
        messages = await ctx.channel.history(limit=None).flatten()

        for m in messages[::-1]:
            lines = [f'\n{m.created_at.strftime("%d/%m/%Y, %H:%M")}\n', f'{m.author}:', f'{m.content}']
            with open('messageLog.txt', 'a+', encoding='utf-8') as f:
                f.write('\n')
                f.writelines(lines)

        await ctx.send('done. file saved as "messageLog.txt"')

    @command()
    @commands.is_owner()
    async def retreive_all_messages(self, ctx):
        await ctx.send('running process...')
        all_messages = []
        await ctx.send('parsing messages...')
        for channel in ctx.guild.channels:
            if channel.id not in self.ignored:
                try:
                    print(f'parsing {channel.name} messages')
                    all_messages += await channel.history(limit=None).flatten()
                except:
                    print(f'failed to get {channel.name} messages')
            else:
                continue

        await ctx.send('parsing done. writing messages in to a text file...')

        for m in all_messages[::-1]:
            with open('messageLog.txt', 'a+', encoding='utf-8') as f:
                f.write('\n')
                f.writelines(m.content)

        await ctx.send('done. file saved as "messageLog.txt"')

    @command()
    @commands.is_owner()
    async def l(self, ctx):
        await ctx.send('покеда')
        await ctx.channel.leave()

    @command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, m: discord.Member, thread: discord.Thread = None):
        thread = ctx.channel if not thread else thread

        await thread.add_user(m)

    @command()
    @commands.has_permissions(administrator=True)
    async def rem(self, ctx, m: discord.Member, thread: discord.Thread = None):
        thread = ctx.channel if not thread else thread

        await thread.remove_user(m)

        









def setup(client):
    client.add_cog(ThreadTool(client))