import discord
from discord.ext import commands



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

class NicknamePrefixChanger(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.roles = {
                    813354741299544095: '🍍 | ',
                    860268394507010088: '🍉 | ',
                    860934762578182174: '🍊 | ',
                    816146742809985054: '✨ | ',
                    839761690727940146: '🍡 | ',
                    802247272803991552: '🍓 | ',
                    861505975298293780: '⌛ | '
                    }

        self.prefixes = ['🍍 | ', '🍉 | ', '🍊 | ', '✨ | ', '🍡 | ', '🍓 | ', '⌛ | ']

    @commands.command()
    @commands.is_owner()
    async def fix(self, ctx, members: commands.Greedy[discord.Member] = None):
        members = ctx.guild.members if not members else members
        updated_members = []
        failed_members = []

        for member in members:
            if member.top_role.id in self.roles:
                try:
                    await member.edit(nick=f'{member.nick[4:]}')
                    updated_members.append(member)
                except:
                    failed_members.append(member)

        um_viewable = ', '.join([m.mention for m in updated_members])
        fm_viewable = ', '.join([m.mention for m in failed_members])
        
        embed = discord.Embed(
            title = 'Фикс завершен',
            description = f'Успешные операции: {um_viewable}\n\nПровалившиеся операции: {fm_viewable}',
            color = 0xffffaa
        )
        await ctx.send(embed=embed)


    # @commands.command()
    # async def update(self, ctx: commands.Context):
    #     updated_members = []
    #     failed_members = []

    #     for member in ctx.guild.members:
    #         if member.top_role.id in self.roles:
    #             if member.nick == None:
    #                 new_n = self.roles[member.top_role.id]+member.name
    #             else:
    #                 if f'{member.nick}'[:4] in self.prefixes:
    #                     n = f'{member.nick}'[4:]
    #                     new_n = self.roles[member.top_role.id]+n
    #                 else:
    #                     new_n = self.roles[member.top_role.id]+f'{member.nick}'
    #             try:
    #                 await member.edit(nick=new_n)
    #                 updated_members.append(member)
    #             except:
    #                 failed_members.append(member)

    #     um_viewable = ', '.join([m.mention for m in updated_members])
    #     fm_viewable = ', '.join([m.mention for m in failed_members])
        
    #     embed = discord.Embed(
    #         titile = 'Обработка завершена',
    #         description = f'Успешные замены: {um_viewable}\n\nНе получилось заменить: {fm_viewable}',
    #         color = 0xffaaff
    #     )
    #     await ctx.send(embed=embed)

            
        
    
        


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            added_roles = get_added_roles(before, after)
            removed_roles = get_removed_roles(before, after)

            if not len(added_roles) == 0:
                if after.top_role.id in self.roles and before.top_role.id not in self.roles:
                    try:
                        if after.nick is not None:
                            await after.edit(nick=f'{self.roles[after.top_role.id]}{after.nick}')
                        else:
                            await after.edit(nick=f'{self.roles[after.top_role.id]}{after.name}')
                    except:
                        print(f'failed to update nickname for {after.name}')
                elif before.top_role != after.top_role and (before.top_role.id in self.roles
                                                        and after.top_role.id in self.roles):
                    if after.nick == None:
                        new_n = self.roles[after.top_role.id]+after.name
                        print('added roles: added nickname')
                    else:
                        if f'{after.nick}'[:4] in self.prefixes:
                            n = f'{after.nick}'[4:]
                            new_n = self.roles[after.top_role.id]+n

                        else:
                            new_n = self.roles[after.top_role.id]+f'{after.nick}'
                    try:
                        await after.edit(nick=new_n)
                    except:
                        print(f'failed to update nickname for {after.name}')
            
            if not len(removed_roles) == 0:
                if before.top_role != after.top_role and (before.top_role.id in self.roles
                                                        and after.top_role.id in self.roles):
                    if after.nick == None:
                        new_n = self.roles[after.top_role.id]+after.name
                    else:
                        if f'{after.nick}'[:4] in self.prefixes:
                            n = f'{after.nick}'[4:]
                            new_n = self.roles[after.top_role.id]+n
                        else:
                            new_n = self.roles[after.top_role.id]+f'{after.nick}'
                    try:
                        await after.edit(nick=new_n)
                    except:
                        print(f'failed to update nickname for {after.name}')
                elif before.top_role.id in self.roles and after.top_role.id not in self.roles:
                    try:
                        await after.edit(nick=f'{after.nick[4:]}')
                    except:
                        print(f'failed to update nickname for {after.name}')
        elif before.nick != after.nick:
            if after.top_role.id in self.roles:
                if after.nick == None:
                    new_n = self.roles[after.top_role.id]+after.name
                else:
                    if f'{after.nick}'[:4] in self.prefixes: # and f'{after.nick}'[:4] != self.roles[after.top_role.id]
                        n = f'{after.nick}'[4:]
                        new_n = self.roles[after.top_role.id]+n
                    else:
                        new_n = self.roles[after.top_role.id]+f'{after.nick}'
                try:
                    await after.edit(nick=new_n)
                except:
                    pass

                        

            


def setup(client):
    client.add_cog(NicknamePrefixChanger(client))