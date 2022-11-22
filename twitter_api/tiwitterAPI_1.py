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


import requests
import os
import json

# To set your environment variables in your terminal run the following line:
os.environ ['BEARER_TOKEN']='keys'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    user_id = 2244994945
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()


key_words=["Object Detection","YOLO","Machine Learning"]
auth = OAuth1("R3HqOpqIo6AcKjDYKD1tpsBzQ", "hw1X2Hv7IlND6eKewSFbFa7SgQ70OpEHKKr7wzvtFDPlFuffVe",f"AAAAAAAAAAAAAAAAAAAAAPnOhgEAAAAAtGmcPuNuqE%2FTStZkA1wcHCmpY%2Bw%3Dn9KHHdFYQJEyBy5sDYNchbCDqiFV5JBRNTtKPPNWpAE9aJ8uyY")
def bearer_oauth(r):
    r.headers["Authorization"]="Bearer {}".format(f"AAAAAAAAAAAAAAAAAAAAAPnOhgEAAAAAtGmcPuNuqE%2FTStZkA1wcHCmpY%2Bw%3Dn9KHHdFYQJEyBy5sDYNchbCDqiFV5JBRNTtKPPNWpAE9aJ8uyY")
    r.headers["User-Agent"]="Mozilla/5.0"
    
    return r
query_params={'query': 'Python',
             'tweet.fields': 'author_id',
             'expansions':'author_id',
             'max_results': '100',
             'user.fields':'created_at,entities,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
             }
url = "https://api.twitter.com/2/tweets/search/recent"#API url
query_params_two=query_params.copy() # next page header
id_had_lst=[]# looped user
user_info_lst=[]# result
key_word_num=0
next=False # flip page
pageNum=0
while key_word_num<len(key_words):
    
    query_params['query']= key_words[key_word_num]
    query_params_two['query']= key_words[key_word_num]
    print("now we are in",query_params['query'])
    time.sleep(random.random()*10)
    if next:# the second page of now searching key word
        r = requests.get(url,auth=bearer_oauth,params=query_params_two)
    else:# the first page of the now searching key word
        
        r = requests.get(url,auth=bearer_oauth,params=query_params)
    js = r.json()
    print(js)
    for one_user in js["includes"]["users"]:
        if one_user["id"] in id_had_lst: #pass the already looped users
            continue
        id_had_lst.append(one_user["id"])
        user_info_lst.append(one_user)
    print("Done one page!")
    if "next_token" not in js["meta"]: #if we have data in next page
        key_word_num+=1
        next=False
        print("finish the {} key word".format(key_word_num))
        continue
    else:
        pageNum+=1
        if pageNum>9:
            key_word_num+=1
            pageNum=0
            next=False
            print("finish the {} key word".format(key_word_num))
            continue
        query_params_two["next_token"] = js["meta"]["next_token"]
        next=True
        continue
pd.DataFrame(user_info_lst).to_csv(r"twitter.csv")