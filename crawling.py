# python3 crawling.py
from typing import List
import praw
from praw.models import MoreComments
import pandas as pd
LIMIT = float("inf")       #DEBUG : change to large number

# web scraping functions
def scrapePosts(post):  #gets data from all posts and top-level comments in each post
    list1 = [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created]

    #looping through comments of a post
    submission = reddit.submission(id=post.id)
    for top_level_comment in submission.comments[0:]: #Note: Comments sorted by Best
        if isinstance(top_level_comment, MoreComments):
            continue
        list2.append(top_level_comment.body)

    postList.append(list1 + list2) # append post info + comments
    list2.clear()

def allSubreddit(keyword,hot):  # searches all subreddits for keyword

    if hot == 0:
        allPosts = reddit.subreddit("/all").search(keyword, limit=LIMIT)
    else:
        allPosts = reddit.subreddit("/all").search(keyword, sort ="hot", limit=LIMIT)

    print("Post Number:")
    count = 1
    for post in allPosts:
        scrapePosts(post)
        print(count)
        count = count + 1

def subredditSearch(subRed, keyword, hot):  # searches specific subreddit for keyword

    if hot == 0:
        if keyword == "":
            allPosts = reddit.subreddit(subRed).new(limit=LIMIT) #sorted by new
        else:
            allPosts = reddit.subreddit(subRed).search(keyword, limit=LIMIT) #sorted by relevance

    else:
        if keyword == "":
            allPosts = reddit.subreddit(subRed).hot(limit=LIMIT)
        else:
            #allPosts = reddit.subreddit(subRed).hot(limit=LIMIT).search(keyword)
            allPosts = reddit.subreddit(subRed).search(keyword,sort="hot", limit=LIMIT)

    print("Post Number:")
    count = 1
    for post in allPosts:
        scrapePosts(post)
        print(count)
        count = count + 1

# authentication
my_client_id = "Q_pq9JUikHu4tof6QnzJoQ"
my_client_secret = "mPFJC9RLRLEJOavJz6Zv7rdaCrmCXQ"
my_user_agent = "crawlingKeywords"
reddit = praw.Reddit(client_id = my_client_id, client_secret= my_client_secret, user_agent= my_user_agent)

#search selection
subRed = input("Type subreddit to search (leave blank for all): ")
keyword = input("Type keyword to search (leave blank for none): ")
hot = input("Sort by Hot posts? (0=No, 1=Yes): ")

# preparing lists to hold data
postList = []
list1 = []
list2 = []
postList.append(['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'Comments:'])

#search either all subreddits or specific
if subRed == "":
    allSubreddit(keyword, hot)
else:
    subredditSearch(subRed, keyword, hot)


# convert postList to datframe and csv file
postList = pd.DataFrame(postList)
postList.to_csv("results.csv", index=False)
print("Crawling finished. Results shown in results.csv")