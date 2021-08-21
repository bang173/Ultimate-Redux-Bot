import discord
from discord.ext import commands
from discord.ext.commands import command
from requests_html import AsyncHTMLSession
import time


class DiscordpySearch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @command()
    async def dpy(self, ctx, v: str, *, tag: str = None):
        start = time.time()
        await ctx.trigger_typing()
        if v in ('latest', 'stable', 'master'):
            url = f'https://discordpy.readthedocs.io/en/{v}/search.html'
        else:
            return
        embed = discord.Embed(
            title = 'Поиск в документации discord.py',
            color = 0xa5ffa4,
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url='https://i.imgur.com/8ciREEh.jpg')
        s = AsyncHTMLSession()

        if tag is not None:
            payload = {'q': tag}
        else:
            payload = {'q': 'discord'}

        r = await s.get(url, params=payload)
        await r.html.arender(sleep=1, keep_page=True, scrolldown=1, timeout=60)
        res = r.html.find('li')

        # filter
        for r in res:
            if ', in API Reference)' not in r.text:
                res.remove(r)
        if len(res) > 1:
            res.remove(res[-1])
        resu = []
        if len(res) > 30:
            for i in range(30):
                resu.append(res[i-1])
        else:
            resu = res
        results = []
        for r in resu:
            for w in {'attribute', 'class', 'property', 'method', 'function', 'exception', 'data'}:
                if w in r.text:
                    results.append({"text": r.text.replace(f'(Python {w}, in API Reference)', ''), "link": [l for l in r.absolute_links][0]})

        resultsViewAble = '\n'.join([f'**[{r["text"]}]({r["link"]})**' for r in results])

        if not len(resultsViewAble) > 4096:
            embed.description = resultsViewAble
        else:
            embed.description = resultsViewAble[0:4093]+'...'

        res_int = len(results)
        embed.add_field(name='Версия', value=v)
        embed.add_field(name='Результатов', value=f'{res_int} (макс.)' if res_int == 30 else res_int)
        end = time.time()
        wasted_time = f'{end-start:.2f}'
        embed.add_field(name='Затрачено времени', value=f'{wasted_time} секунд')
        await ctx.send(embed=embed)






def setup(client):
    client.add_cog(DiscordpySearch(client))