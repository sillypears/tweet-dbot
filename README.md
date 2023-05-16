# lol

## Shit for me to remember

| env var | type |
| --- | --- |
| DISCORD_TOKEN | str|
| CLIENT_ID | int |
| GUILD_ID | int |

docker build --tag tweet_dbot .
docker run tweet_dbot
docker tag tweet_dbot:latest tweet_dbot:v1.2
docker login
docker tag tweet_dbot:latest <userid>/tweet_dbot:latest
docker push <userid>/tweet_dbot
docker run -d -e DISCORD_TOKEN="$DISCORD_TOKEN" -e CLIENT_ID=$CLIENT_ID -e GUILD_ID=$GUILD_ID -e TWEET_CHANNEL_ID=$TWEET_CHANNEL_ID -e CHECK_URL=$CHECK_URL sillypairs/tweet_dbot:latest
