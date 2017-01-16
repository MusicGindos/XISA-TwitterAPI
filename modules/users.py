import time
from twitter import *
from threading import Thread

start_time = time.time()
consumer_key = "1b7veNvOFSLQobADTLDCkqNpD"
consumer_secret = "FbbKPoJUOOb7mBd1mHdOatksrNlcH3tJQbkENDmdjm1eayfM8U"
access_key = "798072331864309765-fcTHr0dBJhIAjWpBaGBC9KqR86nkXN5"
access_secret = "3FtgkmtDLOVf9qdXZi0Crr8G94GTZQKoZOAgL8I9VHdvh"
twitter = Twitter(
    auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))
#
# consumer_key1 = "NsdUnoM8W1ZHEQOylGmaftkJ5"
# consumer_secret1 = "97WQmq4KYI5QahXyomrHyL8mAz7nMK4heHKFe9TK7fmXeD4F7L"
# access_key1 = "798072331864309765-CYMWpbVstu3MNOT8KRiWvBECbmVqHiA"
# access_secret1 = "ZrtkTIYxCLOYdxwNKn3zbdwQ7d6IfzLS7Fa9fBYAG0O1T"
# twitter = Twitter(
#     auth=OAuth(access_key1, access_secret1, consumer_key1, consumer_secret1))
#

# logfile =  open('log.txt', 'w')
# start_time = time.time()
badWords = ["ape","balls","gosh","fag","faggot","merciless","bullshit","clit", "wierdo", "wino", "witch", "worm", "maniac", "racist", "fascist", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot","asshole","booby","bum","butt","boner","cocksucker","cock sucker","busty","bastard","boorish","antankerous","cunning","cynical","indolent","miserly","pompous","procrastinator","sullen","surly","shiftless","bossy","boastful","belligerent","callous","cantankerous","careless","changeable","clinging","compulsive","conservative","cowardly","cruel","deceitful","detached","dishonest","dogmatic","homo","hippie","ignoramus","domineering","finicky","flirtatious","foolish","foolhardy","fussy","greedy","grumpy","gullible","harsh","jealous","jerk","lazy","machiavellian","materialistic","ego","egoist","manic","monkey","parsimonious","patronizing","pervert","ruthless","sarcastic","secretive","selfish","silly","sneaky","stingy","stubborn","stupid","superficial","tactless","timid","touchy","thoughtless","truculent","vague","vain","vengeful","vulgar","aloof","arrogant","impatient","impolite","impulsive","inconsiderate","inconsistent","indecisive","indiscreet","inflexible","interfering","intolerant","irresponsible","obsessive","obstinate","overcritical","overemotional","abominate","afflict","aggressive","darn","agony","endanger","oblique","obscene","offender","ugly","explode","exile","emphatic","cunt","ass","blow","shit","bitch","nigga","hell","whore","dick","piss","pussy","puta","tit","damn","cum","cock","retard","fucking","fuck","motherfucker","sadist"]
# print(len(badWords))
numberOfThreadFinished = 0


def users(word, result):
    q1 = '/"is a ' + word + '/"'
    tweetsWithWord = twitter.search.tweets(q=q1, count=100)['statuses']
    for tweet in tweetsWithWord:
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
            user["tweeter_name"] = tweet["user"]["screen_name"]
            user["count"] = 1
            user["image"] = tweet["user"]["profile_image_url"].replace('_normal', '')
            user["followers_count"] = tweet["user"]["followers_count"]
            result.append(user)
    global numberOfThreadFinished
    numberOfThreadFinished += 1
    print(str(numberOfThreadFinished) + ' Threads finished in ' + str(time.time() - start_time))
    return


def merge_sort(users):
    results = []
    for user in users:
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
    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(badWords[i], results))
            threads[i].start()

    while True:
        if numberOfThreadFinished == 152:
            break

    res = merge_sort(results)
    return res


#print("My program took", time.time() - start_time, "to run")
