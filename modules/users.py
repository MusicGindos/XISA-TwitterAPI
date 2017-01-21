from twitter import *
from threading import Thread
from config import twitterConfig
from config import base
twitter = Twitter(
    auth=OAuth(twitterConfig.users['access_key'], twitterConfig.users['access_secret'], twitterConfig.users['consumer_key'], twitterConfig.users['consumer_secret']))
numberOfThreadFinished = 0


def users(word, result, thread_number):
    try:
        q1 = '/"is a ' + word + '/"'
        tweets = twitter.search.tweets(q=q1, count=100)['statuses']
        for tweet in tweets:
            exist = False
            for user in result:
                if not result:
                    if user["name"] == tweet["user"]["name"]:
                        user["count"] += 1
                        user['texts'].append(tweet['text'])
                        exist = True
                        break
            if not exist:
                user = {}
                user["name"] = tweet["user"]["name"]
                user["twitter_name"] = tweet["user"]["screen_name"]
                user["count"] = 1
                user["image"] = tweet["user"]["profile_image_url"].replace('_normal', '')
                user["followers_count"] = tweet["user"]["followers_count"]
                result.append(user)
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        return
    except Exception as e:
        print('Exception in getUsers at Thread ' + str(thread_number) + ' error message:' + str(e))
        return


def merge_sort(users_array):
    results = []
    for user in users_array:
        exist = False
        if not results:
            results.append(user)
            continue
        for result in results:
            if result["name"] == user["name"]:
                exist = True
                result["count"] += 1
        if not exist:
            results.append(user)
    results.sort(key=lambda x: x['count'], reverse=True)
    return results


def get_users():
    threads = [None] * 152
    results = []
    bad_words = base.badWords
    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(bad_words[i], results, i))
            threads[i].start()
    while True:
        if numberOfThreadFinished == 152:
            break
    res = merge_sort(results)
    return res[:10]
