import tweepy, openai, mysql.connector, time
from important import api_key, api_secret, bearer_token, access_token, access_secret, client_id, client_secret, open_ai, sqlpass


# twitter setup

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


#loop that allows bot to post tweets

while True:
    mycursor.execute("SELECT text FROM prompts ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchmany()[0]
    response = openai.Completion.create(
        engine='text-davinci-001',
        prompt=myresult,
        max_tokens=200,

    )
    text = response.choices[0].text
    api.update_status(text)
    time.sleep(3600)
    


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