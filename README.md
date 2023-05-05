# lol

## Shit for me to remember

| env var | type |
| --- | --- |
| DISCORD_TOKEN | str|
| CLIENT_ID | int |
| GUILD_ID | int |

docker build --tag tweet_dbot .
docker run tweet_dbot
docker tag tweet_dbot:latest tweet_dbot:v1.0
docker login
docker tag tweet_dbot:latest <userid>/tweet_dbot:latest
docker push <userid>/tweet_dbot