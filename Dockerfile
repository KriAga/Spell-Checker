FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y && \
    apt-get install -y  libhunspell-dev

COPY ./requirements.txt /sur/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
