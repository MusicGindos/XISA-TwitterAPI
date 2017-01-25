from twitter import *
from threading import Thread
from config import twitterConfig
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
                user = {'name': tweet["user"]["name"], 'twitter_name': tweet["user"]["screen_name"], 'count': 1, 'image': tweet["user"]["profile_image_url"].replace('_normal', ''), 'followers_count': tweet["user"]["followers_count"]}
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


def sort_by_followers(users_data):
    index = 0
    arr = []
    for user in users_data:
        if user['followers_count'] > 100:
            arr.append(user)
            index += 1
            if index > 9:
                break
    return arr


def get_users():
    threads = [None] * 152
    results = []
    bad_words = twitterConfig.bad_words
    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(bad_words[i], results, i))
            threads[i].start()
    while True:
        if numberOfThreadFinished == 152:
            break
    res = merge_sort(results)
    res = sort_by_followers(res)
    return res
