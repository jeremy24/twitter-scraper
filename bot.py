
import uuid
import requests
import random
import time


from bs4 import BeautifulSoup
from database import Database
from processor import Processor
from datetime import datetime
from os import urandom


import ssl_fix


class Bot:
    def __init__(self):
        print "started"
        # fire up the necessary tools
        self.db = Database()
        print "1"
        self.flagged_words = self.db.get_flagged_words()
        self.processor = Processor(self.flagged_words)
        # local data
        self.tweets_checked = 0
        self.bot_id = uuid.uuid1()
        self.started = datetime.today()
        print "made new bot"

    def __del__(self):
        pass

    def __str__(self):
        pass

    def scrape(self, text):
        text = text.encode('ascii', errors='ignore')
        text = str(text)
        self.tweets_checked += 1
        num_flags = self.processor.handle_tweet(text)
        if num_flags > 0:
            self.db.handle_flag_tweet(text)
            self.db.handle_tweet(text)
        else:
            # add it anyway for now
            self.db.handle_tweet(text)
        # self.db.handle_tweet(text)

    def get_tweets(self, url):
        # setup the twitter api stuff here
        code = requests.get(url)
        text = code.text
        soup = BeautifulSoup(text, "html.parser")
        p_tags = soup.find_all('p', {"class": "tweet-text"})
        msgs = []
        for para in p_tags:
            self.scrape(para.text)

    def stop(self):
        self.db.close()
        uptime = datetime.today() - self.started
        print "Checked: " + str(self.tweets_checked) + " tweets"
        print("Took " + str(uptime))

    def start(self, url):
        url = str(url)
        self.get_tweets(url)
        pass


def delay():
    # min_sleep = random.randint(1, 100) % random.randint(1, 9)
    # max_sleep = random.randint(101, 199) % random.randint(10, 19)
    # max_sleep += random.randint(101, 199) % random.randint(9, 19)
    # if min_sleep == max_sleep or max_sleep < min_sleep:
    #     max_sleep += min_sleep + 2
    # delay_length = int(random.randint(min_sleep, max_sleep))
    # print("Sleeping for: " + str(delay_length) + " seconds")
    # time.sleep(delay_length)
    # print("Continuing")

    lower = random.randint(1, 5)
    upper = random.randint(6, 10)
    delay_length = int(random.randint(lower, upper))
    print("Sleeping for: " + str(delay_length) + " seconds")
    time.sleep(delay_length)
    print("Continuing")


def test():
    bot = Bot()
    db = Database()
    words = set()

    animals = ["cat", "dog", "bird", "giraffe", "horse", "mouse", "gecko"]
    things = ["tv", "car", "table", "chair", "remote", "calculator", "cup", "bowl"]
    colors = ["red", "green", "blue", "purple", "brown", "white", "neon"]
    people = ["me", "trump", "donald", "bush", "carly", "bernie", "obama"]
    school = ["class", "teacher", "prof", "professor", "subject", "grade"]
    items = ["pen", "zipper", "hand", "rope", "cord", "computer", "laptop", "knife"]

    words = words.union(animals, things, colors, people, school, items)

    temps = ["cold", "hot", "warm"]
    weather = ["rain", "sun", "sunny", "damp", "foggy", "snow", "snowing", "fog"]
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    brands = ["samsung", "nike", "atari", "apple", "android", "google", "wexford", "kenmore"]
    electronics = ["phone", "psp", "xbox", "360", "xboxone", "ps4", "ps3", "ds", "ipod"]
    drinks = ["water", "gatorade", "milk", "oj", "creamer", "coffee", "tea", "hotchocolate", "koolaid"]
    roles = ["wizard", "knight", "monk", "fighter", "priest", "monster", "strider", "archer"]
    clothes = ["shirt", "pants", "shirts", "shoes", "shoe", "glove", "gloves", "hat", "hats"]
    food = ["rice", "noodles", "bread", "lettuce", "tomato", "grape", "apple", "orange", "cake"]

    words = words.union(temps, weather, letters, brands, electronics, drinks, roles, clothes, food)

    a = ["age", "ask", "base", "baby", "bay", "child", "color", "copy", "paste", "cut"]
    b = ["dried", "inch", "human", "happy", "forest", "fire", "french", "german"]
    c = ["product", "reach", "info", "late", "larger", "lost", "log", "tree", "grass"]
    d = ["machine", "car", "drier", "driver", "screw", "bolt", "nut", "recording", "lawn"]
    e = ["record", "lower", "middle", "man", "first", "second", "third", "fourth", "fifth"]
    f = ["treasure", "gold", "money", "ring", "jewel", "ruby", "gem", "diamond", "emerald"]
    g = ["south", "north", "east", "west", "shape", "square", "circle", "single", "couple"]

    words = words.union(a, b, c, d, e, f, g)

    words = sorted(words)

    flagged = db.get_flagged_words()
    for flag in flagged:
        flag = str(flag)
        if flag not in words:
            words.append(flag)

    print("Searching for " + str(words.__len__()) + " words")

    url_begin = "https://twitter.com/search?q="
    url_end = "&src=typd&lang=en"

    for word in words:
        url = url_begin + word + url_end
        print("Starting on url " + str(url))
        delay()
        bot.start(url)

    common_words = sorted(db.get_popular_words())
    for word in common_words:
        word = str(word)
        url = url_begin + word + url_end
        # print("Starting on url " + str(url))
        print "Searching for common word:\t" + word
        delay()
        bot.start(url)

    bot.stop()


test()

