import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import command
from datetime import datetime, timedelta



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
            












def setup(client):
    client.add_cog(EmojiTool(client))