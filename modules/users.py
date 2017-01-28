from twitter import *
from threading import Thread
from config import twitterConfig
twitter = Twitter(
    auth=OAuth(twitterConfig.users['access_key'], twitterConfig.users['access_secret'], twitterConfig.users['consumer_key'], twitterConfig.users['consumer_secret']))
numberOfThreadFinished = 0
rate_limit_flag = False


def users(word, result, thread_number):
    try:
        if word[0] in twitterConfig.aeiou:
            q1 = '/"is an ' + word + '/"'
        else:
            q1 = '/"is a ' + word + '/"'
        tweets = twitter.search.tweets(q=q1, count=100)['statuses']
        print('word = ' + word + '  count = ' + str(len(tweets)))
        for tweet in tweets:
            exist = False
            for user in result:
                if not result:
                    if user["name"] == tweet["user"]["name"]:
                        user["count"] += 1
                        user['texts'].append(tweet['text'])
                        exist = True
                        break
            if not exist and tweet["user"]["followers_count"] > 100:
                user = {'name': tweet["user"]["name"], 'twitter_name': tweet["user"]["screen_name"], 'count': 1, 'image': tweet["user"]["profile_image_url"].replace('_normal', ''), 'followers_count': tweet["user"]["followers_count"]}
                result.append(user)
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        return
    except Exception as e:
        if "Rate limit exceeded" in str(e):
            print("Rate limit exceeded")
            global rate_limit_flag
            rate_limit_flag = True
            numberOfThreadFinished += 1
            return
        else:
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
    bad_words = twitterConfig.bad_words
    threads = [None] * len(bad_words)
    results = []

    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(bad_words[i], results, i))
            threads[i].start()
    while True:
        if numberOfThreadFinished == len(bad_words):
            break
    if rate_limit_flag:
        res = {}
        return res
    else:
        res = merge_sort(results)
        return res
