

from database import Database


def seen_words():
    db = Database()
    words = []
    docs = db.get_seen_words()
    links = 0
    largest_count = 0
    largest_link = 0
    word = ""
    link = ""
    for doc in docs:
        words.append(doc["word"])
        if doc["is_link"]:
            largest_link = doc["count"]
            link = doc["word"]
            links += 1
        if doc["count"] > largest_count:
            largest_count = doc["count"]
            word = doc["word"]
    print "\n\nReport"
    print "\tHave seen " + str(words.__len__()) + " unique words"
    print "\t" + str(links) + " of them are links"
    print "\tThe word:\t\"" + str(word) + "\"\twas seen  " + str(largest_count) + " times"
    print "\tThe link:\t" + str(link) + "\twas seen  " + str(largest_link) + " times"
    print "\n"


def test():
    seen_words()

test()
