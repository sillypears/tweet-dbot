class Config(object):
    def __init__(self, token, client, guild, channel):
        self.DISCORD_TOKEN=token
        self.CLIENT_ID=client
        self.GUILD_ID=guild
        self.TWEET_CHANNEL_ID=channel

    def __str__(self):
        return f"d: {self.DISCORD_TOKEN}, g:{self.GUILD_ID}"
