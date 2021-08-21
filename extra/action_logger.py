import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pprint

def get_added_roles(before, after):
    added_roles = []
    for role in after.roles:
        if role not in before.roles:
            added_roles.append(role)
    return added_roles

def get_removed_roles(before, after):
    removed_roles = []
    for role in before.roles:
        if role not in after.roles:
            removed_roles.append(role)
    return removed_roles

async def get_user_from_target(target, action):
    entry = await target.guild.audit_logs(limit=1, action=action).flatten()
    user = entry[0].user
    return user



class ActionLogger(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = {
            'on_msg_del': True,
            'on_msg_edit': True,
            'm_upd_roles': True,
            'm_upd_nick': True,
            'm_upd_profile': True
        }
        self.ignored_channels = [856558217822994492, 841771697845567488, 812720409082331166, 841771615419105290, 871883550566268958]

    async def log(self, smth):
        channel = await self.client.fetch_channel(864956281991594004)
        await channel.send(embed=smth) if type(smth) != str else await channel.send(smth)

    async def mlog(self, smth):
        channel = await self.client.fetch_channel(841771697845567488)
        await channel.send(embed=smth) if type(smth) != str else await channel.send(smth)

    # @commands.command()
    # @commands.is_owner()
    # async def test(self, ctx):
    #     await self.log('test')

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if not payload.cached_message.channel.id in self.ignored_channels:
            if self.config['on_msg_del'] and payload.cached_message is not None:
                if not payload.cached_message.author.bot:

                    embed = discord.Embed(
                        description = 'Сообщение было удалено',
                        color = 0xb53434,
                        timestamp = payload.cached_message.created_at
                    )
                    embed.add_field(name='Содержимое', value=f'```{payload.cached_message.content}```', inline=True)
                    embed.set_author(name=payload.cached_message.author.name, icon_url=payload.cached_message.author.avatar.url)
                    embed.set_footer(text=payload.cached_message.channel.name)

                    await self.mlog(embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if not payload.cached_message.channel.id in self.ignored_channels:
            if self.config['on_msg_edit'] and payload.cached_message is not None:
                if not payload.cached_message.author.bot:
                    before_content = payload.cached_message.content
                    after_content = payload.data.get('content')

                    embed = discord.Embed(
                        description = f'Пользователь изменил __**[сообщение]({payload.cached_message.jump_url})**__',
                        color = 0xffec6b,
                        timestamp = datetime.now()
                    )
                    embed.add_field(name='До', value=f'```{before_content}```', inline=True)
                    embed.add_field(name='После', value=f'```{after_content}```', inline=True)
                    embed.set_author(name=payload.cached_message.author.name, icon_url=payload.cached_message.author.avatar.url)
                    embed.set_footer(text=payload.cached_message.channel.name)

                    await self.mlog(embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.config['m_upd_roles'] and before.roles != after.roles:
            added_roles = ', '.join([r.mention for r in get_added_roles(before, after)]) if len(get_added_roles(before, after)) > 0 else 'Отсутствуют'
            removed_roles = ', '.join([r.mention for r in get_removed_roles(before, after)]) if len(get_removed_roles(before, after)) > 0 else 'Отсутствуют'
            user = await get_user_from_target(after, discord.AuditLogAction.member_role_update)

            embed = discord.Embed(
                description = 'Изменение ролей участника',
                color = 0x96ff9a,
                timestamp = datetime.now()
            )
            embed.add_field(name='Добавленные роли', value=added_roles, inline=True)
            embed.add_field(name='Удаленные роли', value=removed_roles, inline=True)
            embed.add_field(name='Кто изменил', value=f'{user}({user.mention})', inline=True)
            embed.set_author(name=after.name, icon_url=after.avatar.url)
            
            await self.log(embed)

        if self.config['m_upd_nick'] and before.nick != after.nick:
            user = await get_user_from_target(after, discord.AuditLogAction.member_update)

            embed = discord.Embed(
                description = 'Изменение никнейма участника',
                color = 0x12ff2b,
                timestamp = datetime.now()
            )
            embed.add_field(name='До', value=f'```{before.nick if before.nick is not None else before.name}```', inline=True)
            embed.add_field(name='После', value=f'```{after.nick if after.nick is not None else after.name}```', inline=True)
            embed.add_field(name='Кто изменил', value=f'{user}({user.mention})', inline=True)
            embed.set_author(name=after.name, icon_url=after.avatar.url)
            
            await self.log(embed)






def setup(client):
    client.add_cog(ActionLogger(client))