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
