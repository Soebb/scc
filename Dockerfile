FROM python:latest

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y selenium
RUN python -m pip install urllib3 unittest pyrogram tgcrypto
RUN wget -q https://github.com/Soebb/sc/archive/master.tar.gz && tar xf master.tar.gz && rm master.tar.gz

WORKDIR /sc-master
CMD python3 main.py
