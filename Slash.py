import pip
import logging

def install(package):
    pip.main(['install', package])

try:
    from profanity import profanity
except:
    install('profanity')
    from profanity import profanity

try:
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from chatterbot import ChatBot
except:
    install('chatterbot')
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from chatterbot import ChatBot

try:
    import discord
except:
    install('discord.py')
    import discord

print("-------------------")
print("Discord.py version: {}".format(discord.version_info))
print("-------------------")

logging.basicConfig(level=logging.INFO)
client = discord.Client()

chatbot = ChatBot("Slash")
chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

cw = [line.rstrip('\n') for line in open('controversialwords.txt')]
profanity.load_words(cw)

@client.event
async def on_message(message):
    if message.content.startswith(client.user.mention):
        SlashResponse = message.content
        SlashResponse = SlashResponse.replace(client.user.mention, "")
        if profanity.contains_profanity(SlashResponse):
            response = """```ERROR: You cannot send controversial messages using this bot.```"""
        else:
            response = str(chatbot.get_response(SlashResponse))
            if profanity.contains_profanity(response):
                response = str(profanity.censor(response))
        await client.send_message(message.channel, message.author.mention + " " + response)

@client.event
async def on_ready():
    print(' ')
    print('------------------')
    print('Logged in as ' + client.user.name)
    print('ID: ' + client.user.id)
    print('------------------')
    print(' ')
Token = open("token.txt")
client.run(Token.read())
