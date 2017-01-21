from twitter import *
import re
from collections import Counter
from threading import Thread
from config import twitterConfig
from modules import json_reader_writer

twitter = Twitter(
    auth=OAuth(twitterConfig.celebs['access_key'], twitterConfig.celebs['access_secret'], twitterConfig.celebs['consumer_key'], twitterConfig.celebs['consumer_secret']))
numberOfThreadFinished = 0


def get_celebs(word, result, index):
    try:
        celeb_names = []
        celebs_repeat = []
        regex = r"\sis\sa*\s" + word
        q1 = '/"is a ' + word + '/"'
        tweets = twitter.search.tweets(q=q1, count=100)['statuses']
        temp_user = {}
        retweets = 0
        output_obj = {}
        for tweet in tweets:
            output_obj = {'mentions': tweet['entities']['user_mentions'], 'user_name': tweet['user']['screen_name'], 'text': tweet['text'], 'good': {}}
            retweets += tweet['retweet_count']
            matches = re.search(regex, output_obj['text'])
            if matches:
                first_part = re.split(regex, output_obj['text'])[0]
                name = first_part.split(" ")
                first_name = name[-1]
                if first_name and first_name[0].isupper():
                    last_name = first_part[-2]
                    if last_name and last_name[0].isupper():
                        output_obj['good'] = first_name + last_name
                    else:
                        output_obj['good'] = first_name
                if output_obj['good']:
                    celeb_names.append(output_obj['good'])
        output_obj['retweet_count'] = retweets
        if celeb_names:
            celeb_name = Counter(celeb_names).most_common(1)[0]
            if celeb_name[0] not in celebs_repeat:
                celebs_repeat.append(celeb_name[0])
                users = twitter.users.search(q=celeb_name[0], count=20)
                followers_count = 0
                user_name = 'a'
                twitter_name = ' '
                image = 'b'
                for user in users:
                    if user["followers_count"] > followers_count:
                        user_name = user["name"]
                        followers_count = user["followers_count"]
                        twitter_name = user["screen_name"]
                        image = user["profile_image_url"].replace('_normal', '')
            temp_user["name"] = user_name;
            temp_user["twitter_name"] = twitter_name
            temp_user["image"] = image
            temp_user["word"] = word.upper()
            temp_user["retweet_count"] = retweets
        result[index] = temp_user
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        return
    except Exception as e:
        print('Exception in getUsers at Thread ' + str(index+1) + ' error message:' + str(e))
        return


def celebs(category):
    threads = [None] * 10
    results = [None] * 10
    bad_words = json_reader_writer.read_from_data_json("categories", category)
    if bad_words:
        for i in range(len(threads)):
            threads[i] = Thread(target=get_celebs, args=(bad_words[i], results, i))
            threads[i].start()
        while True:
            if numberOfThreadFinished == 10:
                break
    return results
