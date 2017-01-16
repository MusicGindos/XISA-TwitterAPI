from twitter import *
from threading import Thread
from py import twitterConfig

twitter = Twitter(
    auth=OAuth(twitterConfig.user['access_key'], twitterConfig.user['access_secret'], twitterConfig.user['consumer_key'], twitterConfig.user['consumer_secret']))


badWords = ["ape","balls","gosh","fag","faggot","merciless","bullshit","clit", "wierdo", "wino", "witch", "worm", "maniac", "racist", "fascist", "liar", "corrupt", "fat", "misogynist", "chauvinist", "idiot","asshole","booby","bum","butt","boner","cocksucker","cock sucker","busty","bastard","boorish","antankerous","cunning","cynical","indolent","miserly","pompous","procrastinator","sullen","surly","shiftless","bossy","boastful","belligerent","callous","cantankerous","careless","changeable","clinging","compulsive","conservative","cowardly","cruel","deceitful","detached","dishonest","dogmatic","homo","hippie","ignoramus","domineering","finicky","flirtatious","foolish","foolhardy","fussy","greedy","grumpy","gullible","harsh","jealous","jerk","lazy","machiavellian","materialistic","ego","egoist","manic","monkey","parsimonious","patronizing","pervert","ruthless","sarcastic","secretive","selfish","silly","sneaky","stingy","stubborn","stupid","superficial","tactless","timid","touchy","thoughtless","truculent","vague","vain","vengeful","vulgar","aloof","arrogant","impatient","impolite","impulsive","inconsiderate","inconsistent","indecisive","indiscreet","inflexible","interfering","intolerant","irresponsible","obsessive","obstinate","overcritical","overemotional","abominate","afflict","aggressive","darn","agony","endanger","oblique","obscene","offender","ugly","explode","exile","emphatic","cunt","ass","blow","shit","bitch","nigga","hell","whore","dick","piss","pussy","puta","tit","damn","cum","cock","retard","fucking","fuck","motherfucker","sadist"]
result = {}
words_with_texts = []
numberOfThreadFinished = 0
user_details = {'total_bad_words' : 0}
numberOfImages = 0
images = []


def init():
    global result
    result = {}
    global words_with_texts
    words_with_texts = []
    global numberOfThreadFinished
    numberOfThreadFinished = 0
    global user_details
    user_details = {'total_bad_words': 0}
    global numberOfImages
    numberOfImages = 0
    global images
    images= []


def get_tweets_from_user(user_name,page_number):
    global user_details
    global result
    number = 0
    word_res = {}
    try:
        userTweets = twitter.statuses.user_timeline(screen_name=user_name,  count=200, page=page_number)

        if page_number == 1:
            user_details = {'name': userTweets[0]['user']['name'], 'screen_name': userTweets[0]['user']['screen_name'], 'total_bad_words': 0, 'followers_count':userTweets[0]['user']['followers_count'],'image' : userTweets[0]['user']["profile_image_url"].replace('_normal', '')}
            result["user_details"] = user_details
        for tweet in userTweets:
            for word in badWords:
                count = tweet["text"].lower().count(word)
                if count > 0:
                    user_details['total_bad_words'] += count
                    if words_with_texts:
                        for res in words_with_texts:
                            if res['word'] == word:
                                res["count"] += count
                                temp = {}
                                temp["created_time"] = tweet["created_at"]
                                temp["tweet"] = tweet["text"]
                                res["texts"].append(temp)
                                number = 1
                                break
                    if number == 0:
                        word_res["word"] = word
                        word_res["count"] = count
                        word_res["texts"] = []
                        temp = {}
                        temp["created_time"] = tweet["created_at"]
                        temp["tweet"] = tweet["text"]
                        word_res["texts"].append(temp)
                        words_with_texts.append(word_res)
                    global numberOfImages
                    if numberOfImages < 15:
                        split_tweet = tweet["text"].split(' ')
                        for str_word in split_tweet:
                            if numberOfImages > 15:
                                break
                            if str_word[0] == '@':
                                temp_str = str_word
                                if temp_str[-1:] == ':':
                                    temp_str = temp_str[:-1]
                                if temp_str not in result:
                                    try:
                                        user = twitter.statuses.user_timeline(screen_name=temp_str[1:], count=1)
                                        images.append(user[0]["user"]["profile_image_url"].replace('_normal', ''))
                                        numberOfImages += 1
                                    except:
                                        print("user not found")
                word_res = {}
                temp = {}
                number = 0
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        return
    except IndexError:
        numberOfThreadFinished += 1
        return
    except:
        numberOfThreadFinished += 1
        return

def get_user(screen_name):
    init()
    threads = [None] * 16
    for i in range(len(threads)):
        threads[i] = Thread(target=get_tweets_from_user, args=(screen_name, i+1))
        threads[i].start()

    while True:
        if numberOfThreadFinished == 16:
            print('done all')
            words_with_texts.sort(key=lambda x: x['count'], reverse=True)
            result["images"] = list(set(images)) #remove duplicates
            result["words_with_texts"] = words_with_texts[:5]
            break

    return result