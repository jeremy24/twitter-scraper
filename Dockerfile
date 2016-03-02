
FROM ubuntu

MAINTAINER Jeremy Poff

# update and install needed pieces
RUN apt-get update #redo
RUN apt-get install -y tar git openssl curl nano wget dialog net-tools build-essential python python-dev python-distribute python-pip


# set dir to /home and clone down the code from github
WORKDIR /home/apps 

RUN git clone https://github.com/jeremy24/twitter-scraper.git

# cd into the bot folder and install deps
#redo
WORKDIR /home/apps/twitter-scraper 

RUN pip install -r package_list.txt 

# start the bot
CMD python bot.py 
