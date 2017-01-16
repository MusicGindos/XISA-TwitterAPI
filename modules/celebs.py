from twitter import *
import re
from collections import Counter
from threading import Thread
from py import twitterConfig

twitter = Twitter(
    auth=OAuth(twitterConfig.celebs['access_key'], twitterConfig.celebs['access_secret'], twitterConfig.celebs['consumer_key'], twitterConfig.celebs['consumer_secret']))

numberOfThreadFinished = 0

def get_celebs(word, result, index):
    celebNames = []
    celebsRepeat = []
    regex = r"\sis\sa*\s" + word
    q1 = '/"is a ' + word + '/"'
    tweetsWithWord = twitter.search.tweets(q=q1, count=100)['statuses']
    tempUser = {}
    retweets = 0
    for tweet in tweetsWithWord:
        outputObj = {'mentions': tweet['entities']['user_mentions'], 'userName': tweet['user']['screen_name'],
                     'text': tweet['text'], 'good': {}}
        retweets += tweet['retweet_count']
        matches = re.search(regex, outputObj['text'])
        if matches:
            firstPart = re.split(regex, outputObj['text'])[0]
            name = firstPart.split(" ")
            firstName = name[-1]
            if firstName and firstName[0].isupper():
                lastName = firstPart[-2]
                if lastName and lastName[0].isupper():
                    outputObj['good'] = firstName + lastName
                else:
                    outputObj['good'] = firstName
            if outputObj['good']:
                celebNames.append(outputObj['good'])
    outputObj['retweet_count'] = retweets
    if celebNames:
        celebName = Counter(celebNames).most_common(1)[0]
        if celebName[0] not in celebsRepeat:
            celebsRepeat.append(celebName[0])
            users = twitter.users.search(q=celebName[0], count=20)
            followers_count = 0
            userName = 'a'
            image = 'b'
            for user in users:
                if user["followers_count"] > followers_count:
                    userName = user["name"]
                    followers_count = user["followers_count"]
                    image = user["profile_image_url"].replace('_normal', '')
        tempUser["name"] = userName;
        tempUser["image"] = image
        tempUser["word"] = word.upper()
        tempUser["retweet_count"] = retweets
    result[index] = tempUser
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    return


def celebs():
    threads = [None] * 10
    results = [None] * 10
    badWords = ["racist", "fascist", "ugly", "stupid", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot"]
    for i in range(len(threads)):
        threads[i] = Thread(target=get_celebs, args=(badWords[i], results, i))
        threads[i].start()

    while True:
        if numberOfThreadFinished == 10:
            break
    return results
