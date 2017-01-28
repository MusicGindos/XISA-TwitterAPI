from twitter import *
from threading import Thread
from config import twitterConfig
from modules import json_reader_writer
twitter = Twitter(
    auth=OAuth(twitterConfig.celeb['access_key'], twitterConfig.celeb['access_secret'], twitterConfig.celeb['consumer_key'], twitterConfig.celeb['consumer_secret']))
numberOfThreadFinished = 0
total_bad_tweets = 0

def init():
    global numberOfThreadFinished
    numberOfThreadFinished = 0


def get_tweets(name, word, result, index):
    texts = {}
    phrase = '/"' + name + ' is a ' + word + '/"'
    tweets = twitter.search.tweets(q=phrase, count=100)['statuses']
    global total_bad_tweets
    total_bad_tweets += len(tweets)
    print(len(tweets))
    texts[word] = {'word': word, 'texts': [], 'bad_words_count': 0}
    texts_array = []
    for tweet in tweets:
        if tweet['text'] not in texts_array:
            texts_array.append(tweet['text'])
            obj = {"tweet": tweet['text'], "tweet_id": tweet["id_str"], "created_time": tweet["created_at"], "name": tweet['user']["name"], "twitter_name": tweet['user']["screen_name"]}
            texts[word]['texts'].append(obj)
    bad_words_count = 0
    for text in texts[word]['texts']:
        bad_words_count += text["tweet"].count(word)
    texts[word]['bad_words_count'] = bad_words_count
    texts[word]['texts'] = texts[word]['texts'][:10]
    if texts[word]['bad_words_count'] is not 0:
        result[index] = texts[word]
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    return


def celeb_tweets(name, category, twitter_name="realDonaldTrump"):
    if json_reader_writer.is_category(category):
        bad_words = json_reader_writer.read_from_data_json("categories", category)
        user = twitter.statuses.user_timeline(screen_name=twitter_name, count=1, page=0)
        celeb = {"name": user[0]['user']['name'], "twitter_name": user[0]['user']['screen_name'], "image": user[0]['user']["profile_image_url"].replace('_normal', ''), "followers_count": user[0]['user']['followers_count']}

        threads = [None] * 10
        results = [None] * 10
        for i in range(len(threads)):
            threads[i] = Thread(target=get_tweets, args=(name, bad_words[i], results, i))
            threads[i].start()
        most_used_word = ''
        while True:
            if numberOfThreadFinished == 10:
                if results:
                    if any(results):
                        #results = filter(None, results)
                        results = [x for x in results if x != None]
                        results.sort(key=lambda x: x['bad_words_count'], reverse=True)
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
        return res
    else:
        return []
