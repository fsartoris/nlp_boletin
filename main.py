
import spacy
import scrapper
import logging

from datetime import date
from nlp import parse_money
from nlp import parse_business
from twitter_api import tweet_data
from functions import format_money

def boletin(fecha):

    try:

        result = scrapper.parse_contrataciones('https://www.boletinoficial.gob.ar', fecha)

        nlp_spacy = spacy.load("es_core_news_md")

        for key, value in result.items():
            money = parse_money(value)
            business = parse_business(nlp_spacy, value)

            if len(business) > 0:
                for b in business:
                    tweet = "Empresa contratada: %s\nImporte: %s\nFuente: %s" % \
                            (b.upper(), format_money(money), key)
                    tweet_data(tweet)

    except Exception as e:
        logging.error('Error at %s', exc_info=e)


def main():
    boletin(date.today().strftime("%Y%m%d"))

if __name__ == '__main__':
    main()
