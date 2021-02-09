FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y && \
    apt-get install -y  libhunspell-dev vim gzip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
RUN wget https://kagapa.s3.ap-south-1.amazonaws.com/ml/marathi_bigram_count.txt.gz
RUN gunzip marathi_bigram_count.txt .gz
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
