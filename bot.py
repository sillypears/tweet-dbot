import discord
import os
from config import app_config
from discord import app_commands
import requests

conf = app_config['dev'] if os.environ.get('DEBUG') == True else app_config['prd'] 
MY_GUILD = discord.Object(id=conf.GUILD_ID)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


@client.tree.command(name='clear')
# @app_commands.describe(text_to_send='Clear them tweets')
async def clear_tweets(interaction: discord.Interaction ):
    """ Clear Tweets lol """
    res = requests.post('http://192.168.1.55:4999/clearNewTweets')
    await interaction.response.send_message(f"Cleared {res.json()['cleared']} tweets!");
    # await interaction.response.send_message("Hello!")

@client.tree.context_menu(name='Clear Tweets')
@app_commands.describe(text_to_send='Clear them tweets')
async def test(interaction: discord.Interaction, message: discord.Message):
    res = requests.post('http://192.168.1.55:4999/clearNewTweets')
    await interaction.response.send_message(f"Cleared {res.json()['cleared']} tweets!");

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(conf.DISCORD_TOKEN)