import discord
from discord.ext import commands

from src.Entry import Entry
from src import embeds, secrets

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
        participants[author] = Entry()
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
            msgs.append(f"\u2022 {str(user.name)}")
        await ctx.send("\n".join(msgs))
    else:
        await ctx.send("Nobody has joined yet")


# Add an address to your entry
@bot.command(pass_context=True)
async def addr(ctx, *, arg):
    if ctx.author in participants.keys():
        participants[ctx.author].address = arg
        await ctx.send(embed=embeds.address(arg))
    else:
        await ctx.send(embed=embeds.not_joined)


# Catch error if no argument is passed to addr()
@addr.error
async def addr_error(ctx, _):
    if ctx.author in participants.keys():
        await ctx.send(embed=embeds.no_address)
    else:
        await ctx.send(embed=embeds.not_joined)


@bot.command(name='confirm-addr', pass_context=True)
async def confirm_addr(ctx):
    if ctx.author in participants.keys():
        if participants[ctx.author].address is not None:
            await ctx.send(embed=embeds.confirm_addr)
        else:
            await ctx.send(embed=embeds.no_address)
    else:
        await ctx.send(embed=embeds.not_joined)


bot.run(secrets.token)
