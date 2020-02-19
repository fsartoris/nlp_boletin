import os
import tweepy as tw

consumer_key= 'your_key_here'
consumer_secret= 'your_key_here'
access_token= 'your_key_here'
access_token_secret= 'your_key_here'

def tweet_data(text):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    api.update_status(text)
