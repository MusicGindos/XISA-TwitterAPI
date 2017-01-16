from twitter import *
import json
from threading import Thread
from py import twitterConfig

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
    for tweet in tweets:
        if tweet['text'] not in texts[word]['texts']:
            texts[word]['texts'].append(tweet['text'])
    bad_words_count = 0
    for text in texts[word]['texts']:
        bad_words_count += text.count(word)
    texts[word]['bad_words_count'] = bad_words_count
    result[index] = texts[word]
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    return


def celeb_tweets(name):
    users = twitter.users.search(q=name, count=10)
    followers_count = 0
    userName = ' '
    image = ' '
    celeb = {}
    for user in users:
        if user["followers_count"] > followers_count:
            celeb["name"] = user["name"]
            celeb["twitter_name"] = user['screen_name']
            celeb["image"] = user["profile_image_url"].replace('_normal', '')
            followers_count = user["followers_count"]


    threads = [None] * 10
    results = [None] * 10
    badWords = ["racist", "fascist", "ugly", "stupid", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot"]
    for i in range(len(threads)):
        threads[i] = Thread(target=get_tweets, args=(name, badWords[i], results, i))
        threads[i].start()

    while True:
        if numberOfThreadFinished == 10:
            results.sort(key=lambda x: x['bad_words_count'], reverse=True)
            break
    res = {}
    res["wordsWithTweets"] = results[1:6]
    res["celeb_details"] = celeb
    res["mostUsedWord"] = results[0]["word"].upper()
    init()
    return res