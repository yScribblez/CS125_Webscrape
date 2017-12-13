import json
import requests
import praw
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.sentiment.util import *

def organize():
    with open('api_keys.json') as f:
        api_keys = json.loads(f.read())

    reddit = praw.Reddit(
        client_id=api_keys['client_id'],
        client_secret=api_keys['client_secret'],
        password=api_keys['password'],
        user_agent=api_keys['user_agent'],
        username=api_keys['username']
        # your info here
    )
    post = {}
    reddit_titles_to_comments = {}
    submissions = reddit.subreddit('all').hot(limit=4) #1 post
    for submission in submissions: #for post in posts
        submission.comments.replace_more(limit=1) #0 means head comments
        for comment in submission.comments.list():
            reddit_titles_to_comments[submission.title] = [comment.body for comment in submission.comments.list()]
        sentences = reddit_titles_to_comments[submission.title]
        sid = SentimentIntensityAnalyzer()
        compound = 0
        for sentence in sentences:
            ss = sid.polarity_scores(sentence)
            compound += (ss['compound'])
        post[submission.title] = ("title: " + str(sid.polarity_scores(submission.title)['compound']), "comments: " + str(compound/len(sentences)))
        #something[submission.title] /= len(sentences)
    print(post)
        #for k in ss:
            #print('{0}: {1}, '.format(k, ss[k]), end='')
        #print()

organize()
