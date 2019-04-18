FROM python:3.6-alpine

RUN adduser -D videos

WORKDIR /home/videos

RUN apk update && apk add git
RUN git clone https://github.com/luheeslo/videos .
RUN python -m venv env
RUN env/bin/pip install --upgrade pip setuptools
RUN env/bin/pip install -e ".[testing]"

RUN chmod +x boot.sh

RUN chown -R videos:videos ./
USER videos

EXPOSE 6543
ENTRYPOINT ["./boot.sh"]
