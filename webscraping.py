import json
import requests
import praw

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
submissions = reddit.subreddit('all').hot(limit=100)



for submission in submissions:
    submission = reddit.submission(url=link)
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        print(comment.body)
# okay so i have currently gathered all the comments from a given submission, but i'm thinking i can do two separate
# analysis here: one in which i analyze title sentiment to comment sentiment, and another where i analyze
# comment sentiment to subreddit to determine which subs have the most positive comment community
