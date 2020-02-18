FROM ubuntu
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev  libhunspell-dev
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
