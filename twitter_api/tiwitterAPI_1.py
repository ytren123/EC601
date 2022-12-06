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

# -*- coding: utf-8 -*-
# Copyright 2018 Twitter, Inc.
# Licensed under the MIT License
# https://opensource.org/licenses/MIT
"""
Module containing the various functions that are used for API calls,
rule generation, and related.
"""

import re
import datetime
import logging
try:
    import ujson as json
except ImportError:
    import json

__all__ = ["gen_rule_payload", "gen_params_from_config",
           "infer_endpoint", "convert_utc_time",
           "validate_count_api", "change_to_count_endpoint"]

logger = logging.getLogger(__name__)

def convert_utc_time(datetime_str):
    """
    Handles datetime argument conversion to the GNIP API format, which is
    `YYYYMMDDHHSS`. Flexible passing of date formats in the following types::
        - YYYYmmDDHHMM
        - YYYY-mm-DD
        - YYYY-mm-DD HH:MM
        - YYYY-mm-DDTHH:MM
    Args:
        datetime_str (str): valid formats are listed above.
    Returns:
        string of GNIP API formatted date.
    Example:
        >>> from searchtweets.utils import convert_utc_time
        >>> convert_utc_time("201708020000")
        '201708020000'
        >>> convert_utc_time("2017-08-02")
        '201708020000'
        >>> convert_utc_time("2017-08-02 00:00")
        '201708020000'
        >>> convert_utc_time("2017-08-02T00:00")
        '201708020000'
    """
    if not datetime_str:
        return None
    if not set(['-', ':']) & set(datetime_str):
        _date = datetime.datetime.strptime(datetime_str, "%Y%m%d%H%M")
    else:
        try:
            if "T" in datetime_str:
                # command line with 'T'
                datetime_str = datetime_str.replace('T', ' ')
            _date = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            _date = datetime.datetime.strptime(datetime_str, "%Y-%m-%d")
    return _date.strftime("%Y%m%d%H%M")


def change_to_count_endpoint(endpoint):
    """Utility function to change a normal endpoint to a ``count`` api
    endpoint. Returns the same endpoint if it's already a valid count endpoint.
    Args:
        endpoint (str): your api endpoint
    Returns:
        str: the modified endpoint for a count endpoint.
    """

    tokens = filter(lambda x: x != '', re.split("[/:]", endpoint))
    filt_tokens = list(filter(lambda x: x != "https", tokens))
    last = filt_tokens[-1].split('.')[0]  # removes .json on the endpoint
    filt_tokens[-1] = last  # changes from *.json -> '' for changing input
    if last == 'counts':
        return endpoint
    else:
        return "https://" + '/'.join(filt_tokens) + '/' + "counts.json"


def gen_rule_payload(pt_rule, results_per_call=None,
                     from_date=None, to_date=None, count_bucket=None,
                     tag=None,
                     stringify=True):

    """
    Generates the dict or json payload for a PowerTrack rule.
    Args:
        pt_rule (str): The string version of a powertrack rule,
            e.g., "beyonce has:geo". Accepts multi-line strings
            for ease of entry.
        results_per_call (int): number of tweets or counts returned per API
        call. This maps to the ``maxResults`` search API parameter.
            Defaults to 100.
        from_date (str or None): Date format as specified by
            `convert_utc_time` for the starting time of your search.
        to_date (str or None): date format as specified by `convert_utc_time`
            for the end time of your search.
        count_bucket (str or None): If using the counts api endpoint,
            will define the count bucket for which tweets are aggregated.
        stringify (bool): specifies the return type, `dict`
            or json-formatted `str`.
    Example:
        >>> from searchtweets.utils import gen_rule_payload
        >>> gen_rule_payload("beyonce has:geo",
            ...              from_date="2017-08-21",
            ...              to_date="2017-08-22")
        '{"query":"beyonce has:geo","maxResults":100,"toDate":"201708220000","fromDate":"201708210000"}'
    """

    pt_rule = ' '.join(pt_rule.split())  # allows multi-line strings
    payload = {"query": pt_rule}
    if results_per_call is not None and isinstance(results_per_call, int) is True:
        payload["maxResults"] = results_per_call
    if to_date:
        payload["toDate"] = convert_utc_time(to_date)
    if from_date:
        payload["fromDate"] = convert_utc_time(from_date)
    if count_bucket:
        if set(["day", "hour", "minute"]) & set([count_bucket]):
            payload["bucket"] = count_bucket
            try:
                del payload["maxResults"] #Remove if a counts request
            except:
                pass
        else:
            logger.error("invalid count bucket: provided {}"
                         .format(count_bucket))
            raise ValueError
    if tag:
        payload["tag"] = tag

    return json.dumps(payload) if stringify else payload


def gen_params_from_config(config_dict):
    """
    Generates parameters for a ResultStream from a dictionary.
    """

    if config_dict.get("count_bucket"):
        logger.warning("change your endpoint to the count endpoint; this is "
                       "default behavior when the count bucket "
                       "field is defined")
        endpoint = change_to_count_endpoint(config_dict.get("endpoint"))
    else:
        endpoint = config_dict.get("endpoint")


    def intify(arg):
        if not isinstance(arg, int) and arg is not None:
            return int(arg)
        else:
            return arg

    # this parameter comes in as a string when it's parsed
    results_per_call = intify(config_dict.get("results_per_call", None))

    rule = gen_rule_payload(pt_rule=config_dict["pt_rule"],
                            from_date=config_dict.get("from_date", None),
                            to_date=config_dict.get("to_date", None),
                            results_per_call=results_per_call,
                            count_bucket=config_dict.get("count_bucket", None))

    _dict = {"endpoint": endpoint,
             "username": config_dict.get("username"),
             "password": config_dict.get("password"),
             "bearer_token": config_dict.get("bearer_token"),
             "extra_headers_dict": config_dict.get("extra_headers_dict",None),
             "rule_payload": rule,
             "results_per_file": intify(config_dict.get("results_per_file")),
             "max_results": intify(config_dict.get("max_results")),
             "max_pages": intify(config_dict.get("max_pages", None))}
    return _dict


def infer_endpoint(rule_payload):
    """
    Infer which endpoint should be used for a given rule payload.
    """
    bucket = (rule_payload if isinstance(rule_payload, dict)
              else json.loads(rule_payload)).get("bucket")
    return "counts" if bucket else "search"


def validate_count_api(rule_payload, endpoint):
    """
    Ensures that the counts api is set correctly in a payload.
    """
    rule = (rule_payload if isinstance(rule_payload, dict)
            else json.loads(rule_payload))
    bucket = rule.get('bucket')
    counts = set(endpoint.split("/")) & {"counts.json"}
    if len(counts) == 0:
        if bucket is not None:
            msg = ("""There is a count bucket present in your payload,
                   but you are using not using the counts API.
                   Please check your endpoints and try again""")
            logger.error(msg)
            raise ValueError