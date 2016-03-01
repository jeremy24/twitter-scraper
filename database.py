
from pymongo import MongoClient
from pymongo import ReturnDocument
from datetime import datetime


# TODO change flush cache into a batch update, with upsert
class Database:
    MAX_WORD_CACHE_SIZE = 500
    POPULAR_WORDS_TO_GET = 100

    def __init__(self):
        # database connection
        self.client = MongoClient("192.168.2.14", 27017)
        self.db = self.client.twitter_bot
        # local data
        self.word_cache = []
        self.flagged_words = []
        # collections
        self.flagged_words_coll = self.db.flagged_words
        self.flagged_words_coll.ensure_index("word", unique=True)

    # on delete.  flush the cache and
    #   close the db connection
    def __del__(self):
        # flush any final updates
        self.flush_cache()
        self.client.close()

    #  the print method for this class
    def __str__(self):
        return "Connection:" + \
               "\n\tCache Size: " + str(self.word_cache.__len__()) + \
               "\n\tFlagged Words: " + str(self.flagged_words.__len__())

    # a cleaner way to close the connection
    def close(self):
        self.flush_cache()
        self.client.close()

    def handle_flag_tweet(self, text):
        print "handling flagged tweet:  " + str(text)
        words = str(text).split(" ")
        for word in words:
            word = str(word)
            is_href = False
            is_hashtag = False
            is_handle = False
            if "http" in word or "https" in word:
                is_href = True
            if "@" in word:
                is_handle = True
            if "#" in word:
                is_hashtag = True

            doc = self.db.seen_with_flags.find_one(
                {
                    "word": word
                }
            )

            if str(doc) == "none" or str(doc) == "None":
                doc = self.db.seen_with_flags.insert(
                    {
                        "word": str(word),
                        "count": 1,
                        "added_on": datetime.today(),
                        "is_link": is_href,
                        "is_handle": is_handle,
                        "is_hashtag": is_hashtag
                    }
                )
            else:
                doc = self.db.seen_with_flags.update(
                    {
                        "word": word
                    },
                    {
                        "$inc": {
                            "count": 1
                        }
                    }
                )

    def get_popular_words(self):
        m = self.POPULAR_WORDS_TO_GET
        words = []
        docs = self.db.words_seen.find(
            {
                "count": {
                    "$gt": 100
                },
                "is_handle": False,
                "is_link": False,
                "is_hashtag": False
            }
        )
        for doc in docs:
            words.append(doc["word"])
        if words.__len__() > m:
            words = words[0:m]
            print "Found " + str(words.__len__()) + " common words"
            return words
        else:
            docs = self.db.seen_with_flags.find(
                {
                    "count": {
                        "$gt": 50
                    },
                    "is_handle": False,
                    "is_link": False,
                    "is_hashtag": False
                }
            )
            for doc in docs:
                words.append(doc["word"])
            if words.__len__() > m:
                words = words[0:m]
            print "Found " + str(words.__len__()) + " common words"
            return words

    # insert a single word into the db,
    #  update if it already exists
    def insert_word(self, word):
        # print "Inserting: " + word
        word = str(word)

        doc = self.db.words_seen.find_one(
            {
                "word": word
            }
        )
        # print "found " + str(doc)
        is_href = False
        is_hashtag = False
        is_handle = False
        if "http" in word or "https" in word:
            is_href = True
        if "@" in word:
            is_handle = True
        if "#" in word:
            is_hashtag = True

        if str(doc) == "none" or str(doc) == "None":
            doc = self.db.words_seen.insert(
                {
                    "word": word,
                    "count": 1,
                    "added_on": datetime.today(),
                    "is_link": is_href,
                    "is_handle": is_handle,
                    "is_hashtag": is_hashtag
                }
            )
            # print "inserted " + str(doc)
        else:
            doc = self.db.words_seen.update(
                {
                    "word": word
                },
                {
                    "$inc": {
                        "count": 1
                    },
                    "$set": {
                        "is_link": is_href,
                        "is_handle": is_handle,
                        "is_hashtag": is_hashtag
                    }
                }
            )
            # print "Updated " + str(doc)

    # flush the cached words to the database
    #  and wipe the cache when done
    def flush_cache(self):
        print "Flushing word cache"
        i = self.word_cache.__len__() - 1
        for word in self.word_cache:
            self.insert_word(self.word_cache.pop())
            self.insert_word(word)
        self.word_cache[:] = []
        self.db.words_seen.ensure_index("word", unique=True)

    # break into words and add them to the word cache
    # flush the cache after a certain length
    def handle_tweet(self, tweet):
        tweet = str(tweet)
        words = tweet.split(" ")
        for word in words:
            self.word_cache.append(word)

        if self.word_cache.__len__() > self.MAX_WORD_CACHE_SIZE:
            self.flush_cache()

    # grab all of the seen words
    def get_seen_words(self):
        docs = self.db.words_seen.find()
        return docs

    # grab flagged words from db,
    #   serve them from a cache if already loaded
    def get_flagged_words(self):
        docs = self.flagged_words_coll.find()
        words = []
        if self.flagged_words.__len__() > 0:
            return self.flagged_words
        else:
            for doc in docs:
                words.append(str(doc["word"]))
                self.flagged_words.append(str(doc["word"]))
            self.flagged_words = sorted(self.flagged_words)
            return words
