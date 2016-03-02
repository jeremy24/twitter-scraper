
FROM ubuntu

MAINTAINER Jeremy Poff

# update and install needed pieces
RUN apt-get update #r
RUN apt-get install -y tar git openssl curl nano wget dialog net-tools build-essential python python-dev python-distribute python-pip


# set dir to /home and clone down the code from github
WORKDIR /home

RUN git clone https://github.com/jeremy24/twitter-scraper.git

# cd into the bot folder and install deps
#redo
WORKDIR /home/twitter-scraper #redo

RUN /home/twitter-scraper pip install -r package_list.txt #redo

# start the bot
CMD python bot.py 
