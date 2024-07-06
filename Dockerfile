FROM python:3-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir requests

COPY ./xkcd-discord.py ./xkcd-discord.py

CMD [ "python", "./xkcd-discord.py" ]