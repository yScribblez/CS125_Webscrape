mport json
import requests
import praw

with open('api_keys.json') as f:
    api_keys = json.loads(f.read())

reddit_titles_to_comments = {}
reddit_links = []
r = requests.get(
    'https://reddit.com/r/all.json',
    headers={'User-Agents':''}
)
# okay so i have currently gathered all the comments from a given submission, but i'm thinking i can do two separate
# analysis here: one in which i analyze title sentiment to comment sentiment, and another where i analyze
# comment sentiment to subreddit to determine which subs have the most positive comment community
reddit_json = json.loads(r.text)
for x in reddit_json['data']['children']:
    reddit_titles_to_comments[x['data']['title']] = None
    reddit_links.append('https://reddit.com' + x['data']['permalink'])
    
reddit = praw.Reddit(
    # your info here
)
submission = reddit.submission(url=reddit_links[0])
submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
    print(comment.body) # this is every comment in the first post
