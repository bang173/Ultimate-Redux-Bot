import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command
from concurrent.futures import ThreadPoolExecutor


class EmojiTool(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # '\n'.join([f'{field_reacts[index]} {field}' for index, field in enumerate(fields)])

    @command()
    @commands.has_permissions(manage_emojis=True)
    async def show_allowed(self, ctx, emojis: commands.Greedy[discord.Emoji]):
        embed = discord.Embed(
            title = 'Информация о эмодзи',
            description = 'Список разрешенных ролей для эмодзи:',
            color = 0x98befd
        )
        for emoji in emojis:
            roles = ', '.join([role.mention for role in emoji.roles]) if len(emoji.roles) > 0 else 'Эмодзи не заблокировано'
            embed.add_field(
                name = emoji,
                value = roles,
                inline=False
            )
        await ctx.send(embed=embed)



    @command()
    @commands.has_permissions(manage_emojis=True)
    async def manage(self, ctx: commands.Context, option: str, emojis: commands.Greedy[discord.Emoji], roles: commands.Greedy[discord.Role] = None):
        try:
            m = await ctx.send('Выполняется...')
            new_roles = []
            for emoji in emojis:
                if option == 'set':
                    new_roles = roles
                    await emoji.edit(roles=new_roles)
                elif option == 'add':
                    new_roles = emoji.roles + roles
                    await emoji.edit(roles=new_roles)
                elif option == 'remove':
                    for role in emoji.roles:
                        if role not in roles:
                            new_roles.append(role)
                    await emoji.edit(roles=new_roles)
                elif option == 'unlock' and roles is None:
                    await emoji.edit(roles=new_roles)

            emjs = ', '.join([f'{emoji}' for emoji in emojis])
            if option != 'unlock':
                rls = ', '.join([role.mention for role in new_roles]) if len(new_roles) > 0 else 'Эмодзи разблокировано'
                embed = discord.Embed(
                    title = 'Изменение прав на использование эмодзи',
                    description = f'Новое перераспределение прав для эмодзи: {emjs}',
                    color = 0x98befd
                )
                embed.add_field(name='Новые роли', value=rls, inline=False)

            else:
                embed = discord.Embed(description='Эмодзи разблокированы.', color=0x607d8b)

            await m.edit(content='', embed=embed)
            
        except Exception as e:
            print(e)
            

    @command()
    @commands.has_permissions(manage_emojis=True, manage_guild=True)
    async def steal(self, ctx: commands.Context, emojis: commands.Greedy[discord.PartialEmoji], *names):
        start = await ctx.send('Выполняется...')
        messages = [start]
        strings = '_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        ignore = '*'
        if len(emojis) > 0:
            for i, e in enumerate(emojis):
                if len(names) > 0 and names[i] != ignore:
                    e_name = names[i]
                    async def check():
                        for char in names[i]:
                            if char not in strings:
                                await ctx.send(f':x: Недопустимый символ в имени для эмодзи: **{char}**')
                                return True
                        return False
                    loop = asyncio.get_event_loop()
                    with ThreadPoolExecutor() as p:
                        invalid_char_in_name = loop.run_in_executor(p, check)
                    if invalid_char_in_name:
                        e_name = e.name
                else:
                    e_name = e.name

                asset = await e.read()
                try:
                    em = await ctx.guild.create_custom_emoji(name=e_name, image=asset, reason='normal steal')
                    if e_name != e.name:
                        msg = await ctx.send(f':white_check_mark: Добавлен эмодзи {em} под именем "{e_name}"')
                    else:
                        msg = await ctx.send(f':white_check_mark: Добавлен эмодзи {em}')
                    messages.append(msg)
                except Exception as exc:
                    await ctx.send(f'Ошибка добавления:\n{exc}')
            await asyncio.sleep(3)
            for m in messages:
                try:
                    await m.delete(delay=1.0)
                except:
                    pass

        else:
            await ctx.send('Выберите эмодзи')














def setup(client):
    client.add_cog(EmojiTool(client))