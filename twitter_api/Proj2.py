import requests
import os
import json
import numpy as np
from google.cloud import language_v1

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPRuhwEAAAAASI5w1RizbvA82ggDca8DsiutTIY%3DGrAjBZFuovwbsztz4zu0zFg8Wcd8m5IjNiMmsvkVJCRMsEWldZ'

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params_apple = {'query': 'iphone'}
query_params_xiaomi = {'query': 'Xiaomi'}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params_apple)
    dump = json.dumps(json_response, indent=4, sort_keys=True)
    appledatas = json.loads(dump)
    applelist = []
    for datas in appledatas['data']:
        applelist.append(datas['text'])
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tensile-proxy-364720-d84c850e2060.json'
    client = language_v1.LanguageServiceClient()
    apple_sentiment = []
    for text in applelist:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        apple_sentiment.append(sentiment.score)
    apple_average_sentiment = np.average(apple_sentiment)
    print("apple_sentiment:", apple_sentiment)
    # print("Iphone average sentiment: ", apple_average_sentiment)

    json_response = connect_to_endpoint(search_url, query_params_xiaomi)
    dump = json.dumps(json_response, indent=4, sort_keys=True)
    xiaomidatas = json.loads(dump)
    xiaomilist = []
    for datas in xiaomidatas['data']:
        xiaomilist.append(datas['text'])
    client = language_v1.LanguageServiceClient()
    xiaomi_sentiment = []
    for text in xiaomilist:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        xiaomi_sentiment.append(sentiment.score)
    xiaomi_average_sentiment = np.average(xiaomi_sentiment)
    print("Xiaomi_sentiment:", xiaomi_sentiment)
    # print("Xiaomi average sentiment: ", xiaomi_average_sentiment)

if __name__ == "__main__":
    main()