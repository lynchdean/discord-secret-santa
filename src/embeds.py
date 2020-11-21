import discord

nl = "\n"

join = discord.Embed(
    title="Joined!",
    colour=discord.Colour.green(),
    description="You've have joined the Kris Kindle successfully.\n"
                "Please now add your address!"
).add_field(
    name="Add address:",
    value="Use the command `!addr` followed by your address, "
          "using a comma and space (\", \") to separate each line.",
    inline=False
).add_field(
    name="Example:",
    value="`!addr John Smith, 123 Main Street, Rush, K56 AA11, Co. Dublin, Ireland`",
    inline=False
)

already_joined = discord.Embed(
    title="Already joined",
    colour=discord.Colour.red(),
    description=f"You've already joined the Kris Kindle."
)

not_joined = discord.Embed(
    title="You haven't joined the Kris Kindle!",
    colour=discord.Colour.red(),
    description="Type `!join` to join."
)


def address(addr):
    f_addr = ",\n".join(addr.split(", "))
    return discord.Embed(
        title="Address added!",
        colour=discord.Colour.green(),
        description=f"```{f_addr}```"
    ).add_field(
        name="Is this correct?",
        value="If not, use the `!addr` command again with the correct details to overwrite the above \n"
              "\n"
              "If you are happy with your address, type `!confirm-addr`",
        inline=False
    )


no_address = discord.Embed(
    title="No address provided",
    colour=discord.Colour.red(),
    description="Please follow up the `!addr` command with your address, "
                "using a comma and space `\", \"` to separate each line."
).add_field(
    name="Example:",
    value="`!addr John Smith, 123 Main Street, Rush, K56 AA11, Co. Dublin, Ireland`",
    inline=False
)

confirm_addr = discord.Embed(
    title="Address confirmed!",
    colour=discord.Colour.green()
).add_field(
    name="Do you have anyone you need to exclude from drawing?",
    value="If so, type `!exclude`, a space, then type `@` and select the user you want to exclude. "
          "***Do not manually type out the users name.***",
    inline=False,
).add_field(
    name="Example:",
    value="`!exclude @Kris#1234` - where \"@Kris#1234\" should be highlighted in purple.",
    inline=False
)


def user_excluded(user):
    return discord.Embed(
        title=f"{user} successfully added to your exclusions!",
        colour=discord.Colour.green(),
    )


addr_not_confirmed = discord.Embed(
    title="You haven't confirmed your address!",
    description="Please confirm your address before adding exclusions.",
    colour=discord.Colour.red()
)

self_exclude = discord.Embed(
    title="You can't exclude yourself...",
    colour=discord.Colour.red(),
)


def user_removed(user):
    return discord.Embed(
        title=f"{user} successfully removed from your exclusions!",
        colour=discord.Colour.green()
    )


user_not_found = discord.Embed(
    title="User not found.",
    description="The user has not joined yet, or you might have selected the user incorrectly.",
    colour=discord.Colour.red()
)


def user_exclusions(users):
    return discord.Embed(
        title="Your exclusions:",
        description=f"```{nl.join(users)}```",
        colour=discord.Colour.blue()
    )


no_exclusions = discord.Embed(
    title="You have no exclusions.",
    colour=discord.Colour.blue()
)
