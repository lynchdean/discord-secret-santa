import discord
from discord.ext import commands

from src import embeds, secrets
from src.Entry import Entry
from src.draw_async import run_draw

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
        await ctx.send(embed=embeds.msg("Joined! Check your DMs for more info on how to add your address."))
        await author.send(embed=embeds.join)
    else:
        await author.send(embed=embeds.msg("You've already joined the Kris Kindle."))


# Print a list of every user that has successfully joined
@bot.command(pass_context=True)
async def joined(ctx):
    if participants:
        output = []
        for user in participants.keys():
            output.append(str(user))
        await ctx.send(embed=embeds.list_users("Joined:", output))
    else:
        await ctx.send(embed=embeds.msg("Nobody has joined yet."))


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
        await ctx.send(embed=embeds.no_address)
    else:
        await ctx.send(embed=embeds.not_joined)


# This confirms that the user is happy with their entered address and is ready to move to the next step
@bot.command(name='confirm', pass_context=True)
async def confirm(ctx):
    if ctx.author in participants.keys():
        if participants[ctx.author].address is not None:
            participants[ctx.author].confirm()
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
                    await ctx.send(embed=embeds.msg(f"{user} successfully added to your exclusions!"))
                    return
            await ctx.send(embed=embeds.user_not_found)
        else:
            await ctx.send(embed=embeds.msg("You can't exclude yourself..."))
    else:
        await ctx.send(embed=embeds.not_joined)


# Catch error if no argument is passed to exclude(), and provide info on the command
@exclude.error
async def exclude_error(ctx, _):
    if ctx.author in participants.keys():
        await ctx.send(embed=embeds.exclude_info)
    else:
        await ctx.send(embed=embeds.not_joined)


# Undo exclude from a users draw
@bot.command(pass_context=True)
async def unexclude(ctx, *, arg):
    if ctx.author in participants.keys():
        exclusions = participants[ctx.author].exclusions
        exclude_id = int(arg.strip().replace('<@!', '').replace('>', ''))
        if exclude_id in exclusions:
            exclusions.remove(exclude_id)
            member = ctx.guild.get_member(exclude_id)
            await ctx.send(embed=embeds.msg(f"{member} successfully removed from your exclusions."))
        else:
            await ctx.send(embed=embeds.user_not_found)
    else:
        await ctx.send(embed=embeds.not_joined)


# Lists all of a users exclusions
@bot.command(name='my-exclusions', pass_context=True)
async def my_exclusions(ctx):
    if ctx.author in participants.keys():
        exclusions = participants[ctx.author].exclusions
        names = []
        for id in exclusions:
            member = ctx.guild.get_member(id)
            names.append(str(member))
        if names:
            await ctx.send(embed=embeds.list_users("Your exclusions:", names))
        else:
            await ctx.send(embed=embeds.msg("You have no exclusions."))
    else:
        await ctx.send(embed=embeds.not_joined)


# Lists all of a users exclusions
@bot.command(name='all-exclusions', pass_context=True)
async def all_exclusions(ctx):
    output = []
    for user in participants.keys():
        excls = participants[user].exclusions
        if excls:
            excls_str = str([str(ctx.guild.get_member(id)) for id in excls]).strip("[").strip("]")
            output.append(f"{str(user)} -> {excls_str}")
    if output:
        await ctx.send(embed=embeds.list_users("All exclusions:", output))
    else:
        await ctx.send(embed=embeds.msg("There are currently no exclusions."))


@bot.command(pass_context=True)
async def draw(ctx):
    # Check if theres enough people in the draw
    if len(participants.keys()) < 2:
        await ctx.send(embed=embeds.msg("Not enough entries."))
        return

    # Check if everyone has fully confirmed their address
    unconfirmed = []
    for user in participants:
        if not participants[user].confirmed:
            unconfirmed.append(str(user))

    if unconfirmed:
        await ctx.send(embed=embeds.msg("Not all entrants have confirmed their address."))
        return

    # Run the draw and send the results to everybody's DMs
    entries = list(participants.values())
    await run_draw(entries)
    for i in range(len(entries)):
        sender = ctx.guild.get_member(entries[i].id)
        recip_idx = 0 if (i == len(entries) - 1) else (i + 1)
        recip_entry = entries[recip_idx]
        recipient = ctx.guild.get_member(recip_entry.id)
        await sender.send(embed=embeds.result(recipient.name, recip_entry.address))

    await ctx.send(embed=embeds.msg("Draw complete! Check your DMs to see who you got."))

bot.run(secrets.token)
