from twitter import *
from threading import Thread
from config import twitterConfig
twitter = Twitter(  # twitter API oAuth config
    auth=OAuth(twitterConfig.users['access_key'], twitterConfig.users['access_secret'], twitterConfig.users['consumer_key'], twitterConfig.users['consumer_secret']))
numberOfThreadFinished = 0
rate_limit_flag = False


def users(word, result, thread_number):
    try:
        if word[0] in twitterConfig.aeiou:  # if word is a/e/i/o/u the query will be "is an",else "is a"
            q1 = '/"is an ' + word + '/"'
        else:
            q1 = '/"is a ' + word + '/"'
        tweets = twitter.search.tweets(q=q1, count=100)['statuses']  # twitter api call with query
        for tweet in tweets:
            exist = False
            for user in result:
                if not result:
                    if user["name"] == tweet["user"]["name"]:
                        user["count"] += 1
                        user['texts'].append(tweet['text'])
                        exist = True
                        break
            if not exist and tweet["user"]["followers_count"] > 100:  # will insert only 100 followers and up
                user = {'name': tweet["user"]["name"], 'twitter_name': tweet["user"]["screen_name"], 'count': 1, 'image': tweet["user"]["profile_image_url"].replace('_normal', ''), 'followers_count': tweet["user"]["followers_count"]}
                result.append(user)
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        print('Finished:' + str(numberOfThreadFinished))
        return
    except Exception as e:
        if "Rate limit exceeded" in str(e):  # if twitter api in rate limit, will return the newest json from the server
            print("Rate limit exceeded")
            global rate_limit_flag
            rate_limit_flag = True
            numberOfThreadFinished += 1
            return
        else:
            print('Exception in getUsers at Thread ' + str(thread_number) + ' error message:' + str(e))
        return


def merge_sort(users_array):  # merge and sort all the users because of multi-threading
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
    results.sort(key=lambda x: x['count'], reverse=True)  # sort by count of bad words
    return results


def get_users():  #
    bad_words = twitterConfig.bad_words  # get 110 words from data
    print(len(bad_words))
    threads = [None] * (len(bad_words))  # init array of len of bad words
    results = []

    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(bad_words[i], results, i))
            threads[i].start()  # start all thread with multi-threading
    while True:
        if numberOfThreadFinished == (len(bad_words)-2):  # will exit loop when all threads finish
            break
    if rate_limit_flag:
        res = []
        return res
    else:
        res = merge_sort(results)
        return res[:10]
