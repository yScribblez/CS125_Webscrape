import json
import requests
import praw
import nltk
import matplotlib.pyplot as plt
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.sentiment.util import *

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
reddit_titles_to_comments = {}
titles_comm_sent = {}
submissions = reddit.subreddit('all').hot(limit=4)
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend(["https", "could", "even", "like", "get", "would"])
for submission in submissions:
    submission.comments.replace_more(limit=0)    
    reddit_titles_to_comments[submission.title] = [comment.body for comment in submission.comments.list()]

def frequencyDistribution(d):
    words = []
    for post in list(d.values()):
        most_freq = []
        words.extend(nltk.word_tokenize(" ".join(post)))
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    fdist = nltk.FreqDist(words)
    for word, freq in fdist.most_common(10):
        most_freq.append(word)
    plt.figure(figsize=(15, 10))
    my_text = nltk.Text(words)
    my_text.dispersion_plot(most_freq)

def frequencyDistributionAll(d):
    for title, post in d.items():
        most_freq = []
        words = nltk.word_tokenize(" ".join(post))
        words = [word.lower() for word in words if word.isalpha()]
        words = [word for word in words if word not in stop_words]
        fdist = nltk.FreqDist(words)
        for word, freq in fdist.most_common(10):
            most_freq.append(word)
        plt.figure(figsize=(3, 2))
        my_text = nltk.Text(words)
        my_text.dispersion_plot(most_freq)

def organize(reddit_titles_to_comments):
    post = {}
    submissions = reddit.subreddit('all').hot(limit=4) #1 post
    for submission in submissions: #for post in posts
        sentences = reddit_titles_to_comments[submission.title]
        sid = SentimentIntensityAnalyzer()
        compound = 0
        for sentence in sentences:
            ss = sid.polarity_scores(sentence)
            compound += (ss['compound'])
        post[submission.title] = ("title: " + str(sid.polarity_scores(submission.title)['compound']), "comments: " + str(compound/len(sentences)))
    return post

print(organize(reddit_titles_to_comments)) 
frequencyDistribution(reddit_titles_to_comments)
frequencyDistributionAll(reddit_titles_to_comments)
# okay so i have currently gathered all the comments from a given submission, but i'm thinking i can do two separate
# analysis here: one in which i analyze title sentiment to comment sentiment, and another where i analyze
# comment sentiment to subreddit to determine which subs have the most positive comment community
