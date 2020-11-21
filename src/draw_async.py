import random

from src.Entry import Entry


async def run_draw(entries):
    random.shuffle(entries)
    if await no_exceptions(entries):
        return entries
    else:
        await run_draw(entries)


async def no_exceptions(users):
    if users[0].id in users[len(users) - 1].exclusions:
        return False
    for i in range(len(users) - 1):
        if users[i + 1].id in users[i].exclusions:
            return False
    return True


if __name__ == '__main__':
    d = {}

    # Using names here for testing in place of IDs to make it easier to spot potential errors
    names = ["Conor", "Dean", "Dave", "Gav", "Laura", "Riain", "Sean", "Shane", "Shauna"]
    for name in names:
        d[name] = Entry(name)

    d["Dave"].add_exclusion("Laura")
    d["Laura"].add_exclusion("Dave")
    d["Conor"].add_exclusion("Shauna")
    d["Shauna"].add_exclusion("Conor")

    run_draw(d)