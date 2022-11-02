#MINECRAFT CONTROL DISCORD BOT BY MAX PRUDHOMME, 02/11/2022

import discord, time, os, json
from dotenv import load_dotenv
from mcstatus import JavaServer

load_dotenv()
token = os.getenv('TOKEN')
server_IP = os.getenv('SERVER_IP')
server_XMS = os.getenv('SERVER_XMS')
server_XMX = os.getenv('SERVER_XMX')
server_FILE = os.getenv('SERVER_JAR')

intSettings = discord.Intents(messages=True, guilds=True)

client = discord.Client(intents=intSettings)

server = JavaServer.lookup(server_IP)

addPlayerPattern = 'screen -S minecraft -p 0 -X stuff "`printf "whitelist add {}\r"`";'
removePlayerPattern = 'screen -S minecraft -p 0 -X stuff "`printf "whitelist remove {}\r"`";'
serverStartup = 'screen -S minecraft -p 0 -X stuff "`printf "java -jar -Xms{} -Xmx{} {}.jar \r"`";'.format(server_XMS, server_XMX, server_FILE)

@client.event
async def on_connect():
    print("Bot Online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$add'):
        os.system(addPlayerPattern.format(message.content[5:]))
        await message.channel.send(message.content[5:] + " added to the server by " + str(message.author.mention))
        print(message.content[5:] + " added to the server by " + str(message.author))

    if message.content.startswith('$remove'):
        os.system(removePlayerPattern.format(message.content[8:]))
        await message.channel.send(message.content[8:] + " removed from the server by " + str(message.author.mention))
        print(message.content[8:] + " removed from the server by " + str(message.author))

    if message.content.startswith('$server'):
        server = JavaServer.lookup('217.182.8.58')
        if message.content[8:].startswith('start'):
            try:
                status = server.ping()
                await message.channel.send("Hey " + str(message.author.mention) + ", it seems like the server is already running !")
            except:
                os.system(serverStartup)
                await message.channel.send(str(message.author.mention) + " I'm starting the server !")
                print("Server started by " + str(message.author))

        elif message.content[8:].startswith('stop'):
            try:
                status = server.ping()
                os.system('screen -S minecraft -p 0 -X stuff "`printf "stop\r"`";')
                await message.channel.send(str(message.author.mention) + ", I'm stopping the server !")
                print("Server stopped by " + str(message.author))
            except:
                await message.channel.send("Hey " + str(message.author.mention) + ", it seems like the server is already off !")

        elif message.content[8:].startswith('restart'):
            try:
                status = server.ping()
                os.system('screen -S minecraft -p 0 -X stuff "`printf "stop\r"`";')
            except:
                pass
            await message.channel.send(str(message.author.mention) + " I'm restarting the server !")
            time.sleep(5)
            os.system(serverStartup)
            print("Server restarted by " + str(message.author))

        elif message.content[8:].startswith('status'):
            try:
                status = server.status()
                await message.channel.send(str(message.author.mention) + " The server is online.")
            except:
                await message.channel.send(str(message.author.mention) + " The server is offline.")


client.run(token)
