from twitter import *
from threading import Thread
from config import twitterConfig
twitter = Twitter(
    auth=OAuth(twitterConfig.user['access_key'], twitterConfig.user['access_secret'], twitterConfig.user['consumer_key'], twitterConfig.user['consumer_secret']))

result = {}
words_with_texts = []
numberOfThreadFinished = 0
user_details = {'total_bad_words': 0}
numberOfImages = 0
images = []
bad_words = twitterConfig.bad_words


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
    images = []


def unique_images(image_array):
    img_arr = []
    index = 0
    for image in image_array:
        if image not in img_arr and index is not 5:
            img_arr.append(image)
            index += 1
        elif index == 5:
            break
    return img_arr


def count_word(word, string):
    count = 0
    sentence = string.lower()
    sentence = sentence.split(' ')
    for word_splited in sentence:
        if word_splited == word:
            count += 1
    return count


def get_tweets_from_user(user_name, page_number):
    global user_details
    global result
    number = 0
    word_res = {}
    try:
        user_tweets = twitter.statuses.user_timeline(screen_name=user_name, count=200, page=page_number)
        if page_number == 1:
            user_details = {'name': user_tweets[0]['user']['name'], 'screen_name': user_tweets[0]['user']['screen_name'], 'total_bad_words': 0, 'followers_count': user_tweets[0]['user']['followers_count'], 'image': user_tweets[0]['user']["profile_image_url"].replace('_normal', '')}
            result["user_details"] = user_details
        for tweet in user_tweets:
            for word in bad_words:
                count = count_word(word, tweet["text"])
                if count > 0:
                    user_details['total_bad_words'] += count
                    if words_with_texts:
                        for res in words_with_texts:
                            if res['word'] == word:
                                res["count"] += count
                                temp = {'created_time': tweet['created_at'], 'tweet': tweet['text'], 'tweet_id': tweet['id_str'], 'twitter_name': tweet['user']["screen_name"], 'name': tweet['user']['name']}
                                res["texts"].append(temp)
                                number = 1
                                break
                    if number == 0:
                        word_res["word"] = word
                        word_res["count"] = count
                        word_res["texts"] = []
                        temp = {'created_time': tweet['created_at'], 'tweet': tweet['text'], 'tweet_id': tweet['id_str'], 'twitter_name': tweet['user']["screen_name"], 'name': tweet['user']["name"]}
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
                                        image = {'twitter_name': user[0]['user']['screen_name'], 'name': user[0]["user"]["name"], 'image': user[0]["user"]["profile_image_url"].replace('_normal', '')}
                                        images.append(image)
                                        numberOfImages += 1
                                    except Exception as e:
                                        print('Exception in get images at Thread ' + str(page_number + 1) + ' error message:' + str(e))
                                        continue
                word_res = {}
                number = 0
        global numberOfThreadFinished
        numberOfThreadFinished += 1
        return
    except IndexError:
        print(page_number)
        numberOfThreadFinished += 1
        return
    except Exception as e:
        print('Exception in user at Thread ' + str(page_number + 1) + ' error message:' + str(e))
        numberOfThreadFinished += 1
        return


def get_user(screen_name):
    init()
    threads = [None] * 16
    for i in range(len(threads)):
        threads[i] = Thread(target=get_tweets_from_user, args=(screen_name, i))
        threads[i].start()

    while True:
        if numberOfThreadFinished == 16:
            if result:
                if result['user_details']['total_bad_words'] != 0:
                    words_with_texts.sort(key=lambda x: x['count'], reverse=True)
                    result["images"] = unique_images(images)
                    for i in range(5):
                        words_with_texts[i]['texts'] = words_with_texts[i]['texts'][:10]
                    result["words_with_tweets"] = words_with_texts[:5]
            break
    return result
