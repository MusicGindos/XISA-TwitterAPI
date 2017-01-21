from twitter import *
from threading import Thread
from config import twitterConfig
from modules import json_reader_writer
twitter = Twitter(
    auth=OAuth(twitterConfig.celeb['access_key'], twitterConfig.celeb['access_secret'], twitterConfig.celeb['consumer_key'], twitterConfig.celeb['consumer_secret']))

bad_words = ["racist", "fascist", "ugly", "stupid", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot"]
numberOfThreadFinished = 0


def init():
    global numberOfThreadFinished
    numberOfThreadFinished = 0


def get_tweets(name, word, result, index):
    texts = {}
    phrase = '/"' + name + ' is a ' + word + '/"'
    tweets = twitter.search.tweets(q=phrase, count=100)['statuses']
    texts[word] = {'word': word, 'texts': [], 'bad_words_count': 0}
    texts_array = []
    for tweet in tweets:
        if tweet['text'] not in texts_array:
            texts_array.append(tweet['text'])
            obj = {}
            obj["tweet"] = tweet['text']
            obj["tweet_id"] = tweet["id"]
            obj["created_time"] = tweet["created_at"]
            obj["name"] = tweet['user']["name"]
            obj["twitter_name"] = tweet['user']["screen_name"]
            texts[word]['texts'].append(obj)
    bad_words_count = 0
    for text in texts[word]['texts']:
        bad_words_count += text["tweet"].count(word)
    texts[word]['bad_words_count'] = bad_words_count
    result[index] = texts[word]
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    return


def celeb_tweets(name,category):
    if json_reader_writer.is_category(category):
        bad_words = json_reader_writer.read_from_data_json("categories", category)
        users = twitter.users.search(q=name, count=10)
        followers_count = 0
        celeb = {}
        for user in users:
            if user["followers_count"] > followers_count:
                celeb["name"] = user["name"]
                celeb["twitter_name"] = user['screen_name']
                celeb["image"] = user["profile_image_url"].replace('_normal', '')
                followers_count = user["followers_count"]

        threads = [None] * 10
        results = [None] * 10
        for i in range(len(threads)):
            threads[i] = Thread(target=get_tweets, args=(name, bad_words[i], results, i))
            threads[i].start()

        while True:
            if numberOfThreadFinished == 10:
                if results:
                    results.sort(key=lambda x: x['bad_words_count'], reverse=True)
                    break
                else:
                    return {}
        res = {'words_with_tweets': results[1:6], 'user_details': celeb, 'most_used_word': results[0]["word"].upper()}
        # res["words_with_tweets"] = results[1:6]
        # res["user_details"] = celeb
        # res["mostUsedWord"] = results[0]["word"].upper()
        init()
        return res
    else:
        return {}
