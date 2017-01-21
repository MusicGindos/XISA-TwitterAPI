
from twitter import *
from threading import Thread

from py import twitterConfig

twitter = Twitter(
    auth=OAuth(twitterConfig.users['access_key'], twitterConfig.users['access_secret'], twitterConfig.users['consumer_key'], twitterConfig.users['consumer_secret']))


badWords = ["ape","balls","gosh","fag","faggot","merciless","bullshit","clit", "wierdo", "wino", "witch", "worm", "maniac", "racist", "fascist", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot","asshole","booby","bum","butt","boner","cocksucker","cock sucker","busty","bastard","boorish","antankerous","cunning","cynical","indolent","miserly","pompous","procrastinator","sullen","surly","shiftless","bossy","boastful","belligerent","callous","cantankerous","careless","changeable","clinging","compulsive","conservative","cowardly","cruel","deceitful","detached","dishonest","dogmatic","homo","hippie","ignoramus","domineering","finicky","flirtatious","foolish","foolhardy","fussy","greedy","grumpy","gullible","harsh","jealous","jerk","lazy","machiavellian","materialistic","ego","egoist","manic","monkey","parsimonious","patronizing","pervert","ruthless","sarcastic","secretive","selfish","silly","sneaky","stingy","stubborn","stupid","superficial","tactless","timid","touchy","thoughtless","truculent","vague","vain","vengeful","vulgar","aloof","arrogant","impatient","impolite","impulsive","inconsiderate","inconsistent","indecisive","indiscreet","inflexible","interfering","intolerant","irresponsible","obsessive","obstinate","overcritical","overemotional","abominate","afflict","aggressive","darn","agony","endanger","oblique","obscene","offender","ugly","explode","exile","emphatic","cunt","ass","blow","shit","bitch","nigga","hell","whore","dick","piss","pussy","puta","tit","damn","cum","cock","retard","fucking","fuck","motherfucker","sadist"]

numberOfThreadFinished = 0


def users(word, result, thread_number):
    try:
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
    for i in range(len(threads)):
            threads[i] = Thread(target=users, args=(badWords[i], results,i))
            threads[i].start()

    while True:
        if numberOfThreadFinished == 152:
            break

    res = merge_sort(results)
    return res[:10]
