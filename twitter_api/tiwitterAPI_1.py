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
    new_tweets = api.user_timeline(screen_name=screen_name, count=20,  include_rst = False, exclude_replies = True)
      alltweets.extend(new_tweets)
    
    
    oldest = alltweets[-1].id - 1
    
    
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name, count = 20, max_id = oldest, include_rst = False, exclude_replies = True)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))
        
    return alltweets

#I use this code to create a directory
def imagedir(downloaded_images):
    #I need to create a folder for all of my images
    path = os.getcwd() + "/" + downloaded_images
    
    if not(os.path.isdir(path)):
        try:
            os.mkdir(path)
        except OSError:
            print('Directory %s will not be created' % path)
        else:
            shutill.tmtree(path)
            print('Directory %s will be created' % path)
    return path

if __name__ == '__main__':
#I use this code for download images from my twitter account
    path = imagedir('images')
    
    tweets = get_all_tweets('@zwang_z')
    
    #get the url from twitter data
    image_url = set()
    for post in tweets:
        media = post.entities.get('media',[])
        if(len(media) > 0):
            image_url.add(media[0]['media_url'])
            
    for i, url in enumerate(image_url):
        urllib.request.urlretrieve(url, path+'/'+str(i)+'.jpg')