import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageFilter, ImageDraw
from io import BytesIO
import os

def get_invite_by_code(invites, code):
    for i in invites:
        if i.code == code:
            return i

class InviteTrackingSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channels = {
            'log': 0,
            'welcome': 0
        }
        self.invites = {}
        client.loop.create_task(self.cache())


    async def cache(self):
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logchannel = await self.client.fetch_channel(self.channels['log'])
        welcomechannel = await self.client.fetch_channel(self.channels['welcome'])
        embed = discord.Embed(
            description='Присоединился к серверу',
            color=0x98d8ff,
            timestamp=member.joined_at
        )
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        embed.set_footer(text=f'ID: {member.id}')
        try:
            before = self.invites[member.guild.id]
            after = await member.guild.invites()
            self.invites[member.guild.id] = after
            for i in before:
                if i.uses < get_invite_by_code(after, i.code).uses:
                    if i != member.guild.vanity_invite:
                        v = f'Пригласил: {i.inviter.mention} (`{i.inviter}` | `{i.inviter.id}`)\nКод: `{i.code}`\nИспользований: ` {i.uses+1} `'
                    else:
                        v = f'Персональный URL сервера: `{str(member.guild.vanity_invite)}`\nИспользований: `{i.uses}`'
                    embed.add_field(
                        name='Информация о приглашении',
                        value=v
                    )
        except:
            embed.add_field(
                name='Информация о приглашении',
                value='Приглашение удалено либо информация о нем недоступна'
            )

        image = Image.open("assets/bg.jpg")
        img = image.resize((400, 200))
        idraw = ImageDraw.Draw(img)
        f_name = ImageFont.truetype('assets/open-sans.ttf', size = 20)
        f_plain = ImageFont.truetype('assets/pt-sans-bold-italic.ttf', size = 20)
        f_welcome = ImageFont.truetype('assets/micra.ttf', size=19)

        idraw.text((30, 8), 'Добро пожаловать!', font=f_welcome, fill=0x56b5ff)
        idraw.text((90, 50), str(member) if len(str(member)) < 27 else f'{member.name[0:24]+"...#"+member.discriminator}', font=f_name, fill=0x919cff)
        idraw.text((90, 75), f'Ты {member.guild.member_count}-й участник', font=f_name, fill=0x919cff)

        idraw.text((10, 120), 'Желаем приятно провести время!', font=f_plain, fill=0xbf91ff)
        idraw.text((10, 150), f'Аккаунт создан: {member.created_at.strftime("%d/%m/%Y, %H:%M")}', font=f_plain, fill=0xbf91ff)
        
        avatar = member.avatar.replace(size=128)
        avt = BytesIO(await avatar.read())
        imga = Image.open(avt)
        imguser = imga.resize((75, 75))

        img.paste(imguser, (10, 35))
        img.save("u.jpg")
        await logchannel.send(embed=embed)
        await welcomechannel.send(member.mention, file=discord.File('u.jpg'))
        if os.path.exists('u.jpg'):
            os.remove('u.jpg')

    @commands.command()
    @commands.is_owner()
    async def fe(self, ctx):
        await ctx.send('\n'.join([f'{i.code} {i.inviter.id}' for i in await ctx.guild.invites()]))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcomechannel = await self.client.fetch_channel(self.channels['welcome'])
        embed = discord.Embed(
            description='Покинул сервер',
            color=0xce94ff,
            timestamp=member.joined_at
        )
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        await welcomechannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
        except:
            pass









def setup(client):
    client.add_cog(InviteTrackingSystem(client))
