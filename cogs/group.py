from discord.ext import commands
import discord
from datetime import datetime, timedelta
from hashids import Hashids


class Group(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    async def lfglist(self, ctx):
        await ctx.bot.raid.dm_lfgs(ctx.author)
        return

    @discord.ext.commands.command()
    @discord.ext.commands.guild_only()
    async def lfg(self, ctx):
        message = ctx.message
        if '-man' in message.content.lower():
            if message.author.dm_channel is None:
                await message.author.create_dm
            await ctx.bot.help_lfg(message.author.dm_channel)
            await message.delete()
            return
        ctx.bot.raid.add(message)
        role = ctx.bot.raid.get_cell('group_id', message.id, 'the_role')
        name = ctx.bot.raid.get_cell('group_id', message.id, 'name')
        time = datetime.fromtimestamp(ctx.bot.raid.get_cell('group_id', message.id, 'time'))
        is_embed = ctx.bot.raid.get_cell('group_id', message.id, 'is_embed')
        description = ctx.bot.raid.get_cell('group_id', message.id, 'description')
        msg = "{}, {} {}\n{} {}\n{}".format(role, ctx.bot.translations[ctx.bot.args.lang]['lfg']['go'], name,
                                            ctx.bot.translations[ctx.bot.args.lang]['lfg']['at'], time, description)
        if is_embed:
            embed = ctx.bot.raid.make_embed(message, ctx.bot.translations[ctx.bot.args.lang])
            out = await message.channel.send(content=msg)
            await out.edit(content=None, embed=embed)
        else:
            out = await message.channel.send(msg)
        end_time = time + timedelta(seconds=ctx.bot.raid.get_cell('group_id', message.id, 'length'))
        await out.add_reaction('👌')
        await out.add_reaction('❌')
        ctx.bot.raid.set_id(out.id, message.id)
        await ctx.bot.raid.update_group_msg(out, ctx.bot.translations[ctx.bot.args.lang])
        # self.sched.add_job(out.delete, 'date', run_date=end_time, id='{}_del'.format(out.id))
        await message.delete()
        return

    @commands.command(aliases=['editlfg', 'editLfg', 'editLFG'])
    @commands.guild_only()
    async def edit_lfg(self, ctx, arg_id, *args):
        message = ctx.message
        text = message.content.split()
        hashids = Hashids()
        group_id = hashids.decode(arg_id)
        if len(group_id) > 0:
            old_lfg = ctx.bot.raid.get_cell('group_id', group_id[0], 'lfg_channel')
            old_lfg = ctx.bot.get_channel(old_lfg)
            owner = ctx.bot.raid.get_cell('group_id', group_id[0], 'owner')
            if old_lfg is not None and owner is not None:
                old_lfg = await old_lfg.fetch_message(group_id[0])
                if owner == message.author.id:
                    await ctx.bot.raid.edit(message, old_lfg, ctx.bot.translations[ctx.bot.args.lang])
                else:
                    await ctx.bot.check_ownership(message)
                    await message.delete()
            else:
                await message.delete()
        return


def setup(bot):
    bot.add_cog(Group(bot))
