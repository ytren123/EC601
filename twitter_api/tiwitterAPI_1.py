import tweepy
import os
import sys
import subprocess
import urllib.request
from subprocess import call

#These are my Twitter API key
consumer_key = "qIC45ymdG2qll74ExHuuWGhUM"
consumer_secret = "sNbTuogmPfH5Rg9t51c13D8SrZG8KOT5txNp6Nrs8lj9A4kPDz"
access_token = "1039188583154900992-smY4pmpPFSy2DWWyIGYGa6PhqBzmRP"
access_token_secret = "oeDkqE4tp3Xa1lKqaVJYbNuTlKhkHlRtSsJYpfaxn3Bff"

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    alltweets= []
    new_tweets = api.user_timeline(screen_name=screen_name, count=20, )