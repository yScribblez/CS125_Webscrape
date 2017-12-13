import json
import requests
import praw
import nltk
import matplotlib.pyplot as plt
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

#need individual 'api_keys.json' file for authorization
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

number_of_posts = 10
#pull data to create dictionary formatted {title of post : all respective comments} for variable number of posts
reddit_titles_to_comments = {}
submissions = reddit.subreddit('all').hot(limit=number_of_posts)
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

#calculate sentiment proportions for title and respective comments to juxtapose the two
#source: http://opensourceforu.com/2016/12/analysing-sentiments-nltk/ to understand how to calculate sentiment proportions
def organize(reddit_titles_to_comments):
    #dictionary formatted {title of post : average compound sentiment proportion}
    post = {}
    #pull all comments, add to dictionary formatted [title of post : all comments for post]
    submissions = reddit.subreddit('all').hot(limit=4)
    for submission in submissions:
        sentences = reddit_titles_to_comments[submission.title]
        sid = SentimentIntensityAnalyzer()
        #initial total compound
        compound = 0
        for sentence in sentences:
            #calculate proportions for 'negative', 'neutral', 'positive', and 'compound'
            ss = sid.polarity_scores(sentence)
            #add up all compound values
            compound += (ss['compound'])
        #create dictionary of tuple values formatted {title of post : (title: average compound sentiment proportion of title, comments: average compound sentiment proportion of comments}
        post[submission.title] = ("title: " + str(sid.polarity_scores(submission.title)['compound']), "comments: " + str(compound/len(sentences)))
    return post

print(organize(reddit_titles_to_comments))
frequencyDistribution(reddit_titles_to_comments)
frequencyDistributionAll(reddit_titles_to_comments)
