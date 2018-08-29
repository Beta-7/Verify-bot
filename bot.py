import sqlite3
from captcha.image import ImageCaptcha
import random
import string
import discord

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (usrid text, pin text)''')
print("Connecting to table")

image = ImageCaptcha(fonts=['a.ttf'])
text =''
def generate_string(idd):
    random.seed()
    text = ''.join(random.choice(string.digits) for _ in range(4))
    data = image.generate(text)
    image.write(text, 'out.png')
    print(text)
    c.execute("INSERT INTO users  VALUES ('{id}','{pin}')".format(id=idd, pin=text))
    conn.commit()

print("Running discord.py version")
print(discord.__version__)
####################
#  EDIT HERE       #
####################
TOKEN = ''         #
serverid = ''      #
channelid = ''     #
verifiedrole = ''  #
####################
client = discord.Client()
userid = ''
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('test'):
        msg = 'Please write the number on the picture'.format(message)
        msgcnl = 'Messaging {0.author.mention} with instructions'.format(message)
        await client.send_message(message.author, msg)
        await client.send_message(message.channel,msgcnl)
        userid = message.author
        generate_string(message.author.id)
        await client.send_file(message.author, 'out.png')

    if not message.server:
        for row in c.execute('SELECT * FROM users'):
            if message.content.startswith(row[1]):
                serverr = client.get_server(serverid)
                channell = client.get_channel(channelid)
                user = serverr.get_member(row[0])

                print("gud")
                role = discord.utils.get(serverr.roles, name=verifiedrole)
                await client.add_roles(user, role)
                msg = 'Welcome to XXXXX server'.format(message)
                msgcnl = '{0.author.mention} has been verified'.format(message)
                await client.send_message(user, msg)
                await client.send_message(channell,msgcnl)
                c.execute("DELETE FROM users WHERE pin ='{pin}'".format(pin=text))
                conn.commit()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
