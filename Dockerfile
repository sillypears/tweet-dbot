FROM python:3.9.16-bullseye

WORKDIR /src

COPY requirements.txt requirements.txt

ENV DISCORD_TOKEN=
ENV DISCORD_GUILD=
ENV ADMIN_CHANNEL=
ENV DB_URI=
ENV DB_SCHEMA=
ENV DEBUG=True
ENV GOAL=

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3.9", "bot.py"]