import requests
import random
import re
import requests
import threading

from discord.ext import commands
from bs4 import BeautifulSoup as bs

TOKEN = ''
url = ''

page = 'https://www.dotabuff.com/players/'

bot = commands.Bot(command_prefix='!')

miders = ["глеб", "кирилл"]
doters = {'1196584663': '1', '274176160': '1', '142828917': '1', '261454832': '1', '345362238': '1', '107126485': '1', '95091383': '1'}

@bot.command(pass_context=True)
async def insult(ctx, arg):
    res = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json').json()['insult']
    if arg == 'дотеры' or arg == 'doters':
        res = "you`re the best"
    await ctx.send(arg + ', ' + res)

@bot.command(pass_context=False)
async def mider(ctx):
    await ctx.send("Здрасьте, здрасьте люди добрые. Сегодня на мид идет " + miders[random.randrange(0, 2)])

@bot.event
async def on_message(message):
    is_ew0ke = str(message.author) == 'Ew0ke#4034' or str(message.author) == 'Ew0ke#9674'
    dota = (re.search('.*дота*', message.content) is not None or re.search('.*доту*', message.content) is not None) and re.search('.*удал*', message.content) is None
    deleted = re.search('.*удал*', message.content) is not None
    if dota and is_ew0ke:
          await message.channel.send("...")
    if deleted:
          await message.channel.send("Красава стэс")
    await bot.process_commands(message)

def check_doters():
    for id, last in doters.items():
        page = 'https://www.dotabuff.com/players/' + id
        r = requests.get(page, headers={'user-agent': 'Mozilla/5.0'})
        s = bs(r.content, 'html.parser')

        table = s('table')[3]
        nick = table('td')[0].text
        table = s('article')[2]

        hero = re.search('Hero', table.text)
        normal = re.search('Normal', table.text)
        her = table.text[hero.end(): normal.start()]

        result = re.search('Result', table.text)
        match = re.search('Match', table.text)
        res = table.text[result.end(): match.start()-1].lower()

        kda = re.search('KDA', table.text)
        hero = re.search('Hero', table.text[6:])
        KDA = table.text[kda.end(): hero.start() + 6]

        if last != her + KDA:
            doters[id] = her + KDA

            data = {
                "content": nick + " " + res + " match as " + her + " with kda " + KDA,
                "username": "314-ый кабинет"
            }
            requests.post(url, json=data)
    threading.Timer(600.0, check_doters).start()

threading.Timer(5.0, check_doters).start()

bot.run(TOKEN)
