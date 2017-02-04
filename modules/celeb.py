from twitter import *
from threading import Thread
from config import twitterConfig
from modules import json_reader_writer
twitter = Twitter(  # twitter config with oAuth
    auth=OAuth(twitterConfig.celeb['access_key'], twitterConfig.celeb['access_secret'], twitterConfig.celeb['consumer_key'], twitterConfig.celeb['consumer_secret']))
numberOfThreadFinished = 0
total_bad_tweets = 0


def init(): # init for each thread
    global numberOfThreadFinished
    numberOfThreadFinished = 0


def get_tweets(name, word, result, index):  # get name of celeb and word to search nd return tweets about him
    texts = {}
    phrase = '/"' + name + ' is a ' + word + '/"'  # the query to search in twitter
    tweets = twitter.search.tweets(q=phrase, count=100)['statuses']  # twitter search
    global total_bad_tweets
    texts[word] = {'word': word, 'texts': [], 'bad_words_count': 0}
    texts_array = []
    for tweet in tweets:
        if tweet['text'] not in texts_array:
            texts_array.append(tweet['text'])
            obj = {"tweet": tweet['text'], "tweet_id": tweet["id_str"], "created_time": tweet["created_at"], "name": tweet['user']["name"], "twitter_name": tweet['user']["screen_name"]}
            texts[word]['texts'].append(obj)
    bad_words_count = 0
    for text in texts[word]['texts']:
        bad_words_count += text["tweet"].count(word)  # count number of bad words in each text
    texts[word]['bad_words_count'] = bad_words_count
    total_bad_tweets += len(texts[word]["texts"])
    texts[word]['texts'] = texts[word]['texts'][:10]
    if texts[word]['bad_words_count'] is not 0:  # if no bad words -> don't push the dict
        result[index] = texts[word]
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    return


def celeb_tweets(name, category, twitter_name="realDonaldTrump"):
    if json_reader_writer.is_category(category):  # will run only if the category is correct
        bad_words = json_reader_writer.read_from_data_json("categories", category)
        user = twitter.statuses.user_timeline(screen_name=twitter_name, count=1, page=0)  # get the celeb details from twitter api by screen_name
        celeb = {"name": user[0]['user']['name'], "twitter_name": user[0]['user']['screen_name'], "image": user[0]['user']["profile_image_url"].replace('_normal', ''), "followers_count": user[0]['user']['followers_count']}

        threads = [None] * 10  # 10 threads for each word in category
        results = [None] * 10  # array of 10 for each word
        for i in range(len(threads)):
            threads[i] = Thread(target=get_tweets, args=(name, bad_words[i], results, i))
            threads[i].start()  # start 10 thread with multi-threading
        most_used_word = ''
        while True:
            if numberOfThreadFinished == 10:  # wait until all threads to finish their work
                if results:
                    if any(results):
                        results = [x for x in results if x != None]
                        results.sort(key=lambda x: x['bad_words_count'], reverse=True)  # sort by count in bad words
                        try:
                            results = results[1:6]
                        except:
                            results = results[:len(results)]
                        most_used_word = results[0]["word"].upper()
                    else:
                        results = []
                    break
                else:
                    return {}
        res = {'words_with_tweets': results, 'user_details': celeb, 'most_used_word': most_used_word, 'total_bad_tweets': total_bad_tweets}
        init()
        global total_bad_tweets
        total_bad_tweets = 0
        return res
    else:
        return []
