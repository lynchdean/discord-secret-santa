import discord

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
        value="If not, use the `!addr` command again with the correct details to overwrite the above details\n"
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
    name="Do you have anyone you need to exclude?",
    value="If so, type `!exclude` followed by the users Discord username."
          "You can do this multiple times if there is multiple users you need to exclude",
    inline=False
).add_field(
    name="Example:",
    value="`!exclude Kris#1234`",
    inline=False
)

