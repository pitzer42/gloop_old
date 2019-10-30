FROM python:3.7

WORKDIR /usr/src/app

COPY gloop/ gloop/
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN rm requirements.txt

# CMD ["python", "-m", "gloop.match_starter.player_receiver"]
CMD ["ping", "0.0.0.0"]
