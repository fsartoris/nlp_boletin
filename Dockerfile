FROM python:3.6
ADD . /
RUN pip install requests \
    beautifulsoup4 \
    lxml \
    tweepy \
    stop_words \
    spacy

RUN python -m spacy download es_core_news_md
CMD [ "python", "main.py" ]
