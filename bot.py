import tweepy
import openai
import mysql.connector
import time
from time import sleep
from important import api_key, api_secret, bearer_token, access_token, access_secret, client_id, client_secret, open_ai, sqlpass
from config import *


# twitter and ai setup

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
openai.api_key = open_ai


#db setup

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='22Sebastian$',
    database="twitterprompts"
)
mycursor = mydb.cursor()

#set up for loop

search = '#nba'
num_tweets = 10



#loop that allows bot to post tweets from sql database

while True:
    mycursor.execute("SELECT text FROM prompts ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchmany()[0]
    response = openai.Completion.create(
        engine='text-davinci-001',
        prompt=myresult,
        max_tokens=50,

    )
    text = response.choices[0].text
    api.update_status(text)
    time.sleep(30)

    for tweet in api.search_tweets(q=QUERY):
        try:
            print('\nTweet by: @' + tweet.user.screen_name)


            if LIKE:
                if not tweet.favorited:
                    tweet.favorite()
                    print('Liked the tweet')


            if FOLLOW:
                if not tweet.user.following:
                    tweet.user.follow()
                    print('Followed the user')


            if RETWEET:
                if not tweet.retweeted:
                    tweet.retweet()
                    print('Retweeted the tweet')

            sleep(SLEEP_TIME)

        except tweepy.errors.TweepyException as e:
            print(e)

        except StopIteration:
            break



    


#code to add more prompts to database

"""sql = ("INSERT INTO prompts (text) VALUES (%s)")
data = ()

for values in data:
    mycursor.execute(sql, (values,))
mydb.commit()
print(mycursor.rowcount, "record(s) inserted.")

"""



mycursor.execute("SELECT * FROM prompts")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)