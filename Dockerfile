FROM python:3.6-alpine

RUN adduser -D videos

WORKDIR /home/videos

COPY development.ini development.ini
COPY production.ini production.ini
COPY pytest.ini pytest.ini
COPY setup.py setup.py
COPY videos.egg-info videos.egg-info
COPY videos/ videos/
COPY README.txt README.txt
RUN python -m venv env
RUN env/bin/pip install --upgrade pip setuptools
RUN env/bin/pip install -e ".[testing]"

COPY boot.sh ./
RUN chmod +x boot.sh

RUN chown -R videos:videos ./
USER videos

EXPOSE 6543
ENTRYPOINT ["./boot.sh"]
