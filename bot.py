import discord
import os
from discord import app_commands
from discord.ext import tasks
import requests
from config import Config

conf = Config(os.environ.get('DISCORD_TOKEN', 'failure'),os.environ.get('CLIENT_ID', 'failure'),os.environ.get('GUILD_ID', 'failure'), os.environ.get('TWEET_CHANNEL_ID', 'failure'))
MY_GUILD = discord.Object(id=conf.GUILD_ID)
TWEET_CHANNEL = discord.Object(id=conf.TWEET_CHANNEL_ID)
CHECK_URL = os.environ.get('CHECK_URL')

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
        get_tweet_count.start()



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.tree.command(name='clear')
# @app_commands.describe(text_to_send='Clear them tweets')
async def clear_tweets(interaction: discord.Interaction ):
    """ Clear Tweets lol """
    
    try:
        res = requests.post(f"{CHECK_URL}/clearNewTweets")
        if res.status_code == 200:
            await interaction.response.send_message(f"Cleared {res.json()['cleared']} tweets!");
        else:
            await interaction.response.send_message(f"I don't know why this broke: {res.status_code}")
    except Exception as e:
        await interaction.response.send_message(f"Yo shit's broken: {e}");

@client.tree.context_menu(name='Clear Tweets')
@discord.app_commands.describe(text_to_send='Clear them tweets')
async def test(interaction: discord.Interaction, message: discord.Message):
    try:
        res = requests.post(f"{CHECK_URL}/clearNewTweets")
        if res.status_code == 200:
            await interaction.response.send_message(f"Cleared {res.json()['cleared']} tweets!");
        else:
            await interaction.response.send_message(f"I don't know why this broke: e-code {res.status_code}")
    except Exception as e:
        await interaction.response.send_message(f"Yo shit's broken: {e}");

@tasks.loop(minutes=5, count=None)
async def get_tweet_count():
    await client.wait_until_ready()
    res = requests.get(f"{CHECK_URL}/getNewTweets")
    if res.status_code == 200:

        d = res.json()
        try:
            channel = (client.get_channel(TWEET_CHANNEL) or await client.fetch_channel(conf.TWEET_CHANNEL_ID))
            if channel.topic != f"Tweets: {d['newTweets']}":
                print(d, get_tweet_count.count, channel)
                await channel.edit(topic=f"Tweets: {d['newTweets']}")
        except Exception as e:
            print(f"channel is: {e}")
client.run(conf.DISCORD_TOKEN)
