# this checks the tweet for flagged words and decides whether to enter
#   -- is where the learning bit happens


# decides whether or not to act on
#   the data
class Processor:
    def __init__(self, flagged_words):
        self.flagged_words = flagged_words

    def __del__(self):
        pass

    def __str__(self):
        pass

    # take a tweet and return the number of flagged words
    def handle_tweet(self, text):
        words = str(text).split(" ")
        flags_seen = 0
        for word in words:
            if word in self.flagged_words:
                flags_seen += 1
        return flags_seen

