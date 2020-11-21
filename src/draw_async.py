import random


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
