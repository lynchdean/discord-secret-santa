import random

import discord
from discord.ext import commands

from src import embeds, secrets
from src.Entry import Entry

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

participants = {}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# Join the Kris kindle
@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.author
    if author not in participants:
        participants[author] = Entry(author.id)
        embed = embeds.join
        await author.send(embed=embed)
    else:
        embed = embeds.already_joined
        await author.send(embed=embed)


# Print a list of every user that has successfully joined
@bot.command(pass_context=True)
async def joined(ctx):
    if participants:
        msgs = ["Participants:"]
        for user in participants.keys():
            msgs.append(f"\u2022 {str(user)}")
        await ctx.send("\n".join(msgs))
    else:
        await ctx.send("Nobody has joined yet")


# Add an address to your entry
@bot.command(pass_context=True)
async def addr(ctx, *, arg):
    if ctx.author in participants.keys():
        participants[ctx.author].address = arg
        await ctx.author.send(embed=embeds.address(arg))
    else:
        await ctx.author.send(embed=embeds.not_joined)


# Catch error if no argument is passed to addr()
@addr.error
async def addr_error(ctx, _):
    if ctx.author in participants.keys():
        await ctx.author.send(embed=embeds.no_address)
    else:
        await ctx.author.send(embed=embeds.not_joined)


# This confirms that the user is happy with their entered address and is ready to move to the next step
@bot.command(name='confirm-addr', pass_context=True)
async def confirm_addr(ctx):
    if ctx.author in participants.keys():
        if participants[ctx.author].address is not None:
            participants[ctx.author].confirm_addr()
            await ctx.author.send(embed=embeds.confirm_addr)
        else:
            await ctx.author.send(embed=embeds.no_address)
    else:
        await ctx.author.send(embed=embeds.not_joined)


# Exclude a user from your draw
@bot.command(pass_context=True)
async def exclude(ctx, *, arg):
    if ctx.author in participants.keys():
        entry = participants[ctx.author]
        exclude_id = int(arg.strip().replace('<@!', '').replace('>', ''))
        if ctx.author.id != exclude_id:
            for user in participants.keys():
                if user.id == exclude_id:
                    entry.add_exclusion(exclude_id)
                    await ctx.send(embed=embeds.user_excluded(str(user)))
                    return
            await ctx.send(embed=embeds.user_not_found)
        else:
            await ctx.send(embed=embeds.self_exclude)
    else:
        await ctx.send(embed=embeds.not_joined)


@bot.command(pass_context=True)
async def unexclude(ctx, *, arg):
    if ctx.author in participants.keys():
        exclusions = participants[ctx.author].exclusions
        exclude_id = int(arg.strip().replace('<@!', '').replace('>', ''))
        if exclude_id in exclusions:
            exclusions.remove(exclude_id)
            await ctx.send(embed=embeds.user_removed(ctx.guild.get_member(exclude_id)))
        else:
            await ctx.send(embed=embeds.user_not_found)
    else:
        await ctx.send(embed=embeds.not_joined)


@bot.command(name='my-exclusions', pass_context=True)
async def my_exclusions(ctx):
    if ctx.author in participants.keys():
        exclusions = participants[ctx.author].exclusions
        names = []
        for id in exclusions:
            member = ctx.guild.get_member(id)
            names.append(str(member))
        if names:
            await ctx.send(embed=embeds.user_exclusions(names))
        else:
            await ctx.send(embed=embeds.no_exclusions)
    else:
        await ctx.send(embed=embeds.not_joined)


@bot.command(pass_context=True)
async def draw(ctx):
    # Check if theres enough people in the draw
    # if len(participants.keys()) < 3:
    #     await ctx.send("Not enough entries.")
    #     return

    # Check if everyone has fully confirmed their entry
    incomplete = []
    for user in participants:
        if not participants[user].is_complete():
            incomplete.append(str(user))

    if incomplete:
        await ctx.send("Not all users have completed their entry.")
        return

    results = draw(participants)
    print(results)


bot.run(secrets.token)
