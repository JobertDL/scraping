#!/usr/bin/python3

import glob
import http.client
import json
import os
import re
import time
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import sys
import csv

APP_ID = str(sys.argv[1])
APP_SECRET = str(sys.argv[2])


def createFeedUrl(username, APP_ID, APP_SECRET, limit):
    post_args = "/feed?access_token=" + APP_ID + "|" + APP_SECRET + \
                "&fields=attachments,created_time,message&limit=" + str(limit)
    post_url = "https://graph.facebook.com/v3.0/" + username + post_args
    return post_url


def createPostUrl(USER_ID, POST_ID, APP_ID, APP_SECRET):
    post_args = "?access_token=" + APP_ID + "|" + APP_SECRET + \
                "&fields=link,message,created_time,name,story,caption,description,picture,place,shares,source,updated_time"
    post_url = "https://graph.facebook.com/v3.0/" + USER_ID + "_" + POST_ID + post_args
    return post_url


def createPostCommentsUrl(USER_ID, POST_ID, APP_ID, APP_SECRET):
    comments_args = "/comments?access_token=" + APP_ID + "|" + APP_SECRET + \
                    "&order=chronological&limit=1000"
    comments_url = "https://graph.facebook.com/v3.0/" + USER_ID + "_" + POST_ID + comments_args
    return comments_url


def createPostAttachmentsUrl(USER_ID, POST_ID, APP_ID, APP_SECRET):
    attachments_args = "/attachments?access_token=" + APP_ID + "|" + APP_SECRET
    attachments_url = "https://graph.facebook.com/v3.0/" + USER_ID + "_" + POST_ID + attachments_args
    return attachments_url


def getPost(USER_ID, POST_ID):
    post_url = createPostUrl(USER_ID, POST_ID, APP_ID, APP_SECRET)
    print(f"Fetching post: {USER_ID}_{POST_ID}")
    print(f"Post URL: {post_url}")
    try:
        web_response = urllib.request.urlopen(post_url)
        readable_page = web_response.read()
        print(f"Post Response: {readable_page}")
        return json.loads(readable_page)
    except urllib.error.HTTPError as e:
        print(f"HTTPError for {post_url}: {e}")
    except urllib.error.URLError as e:
        print(f"URLError for {post_url}: {e}")
    except Exception as e:
        print(f"Unexpected error for {post_url}: {e}")
    return {}


def getPostComments(USER_ID, POST_ID, n=1):
    data = []
    post_url = createPostCommentsUrl(USER_ID, POST_ID, APP_ID, APP_SECRET)
    print(f"Fetching comments for post: {USER_ID}_{POST_ID}")
    print(f"Comments URL: {post_url}")
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    time.sleep(n)

    try:
        web_response = urllib.request.urlopen(post_url)
        readable_page = web_response.read()
        thisdata = json.loads(readable_page)
        data.extend(thisdata.get('data', []))
    except urllib.error.HTTPError as e:
        print(f"HTTPError for {post_url}: {e}")
    except urllib.error.URLError as e:
        print(f"URLError for {post_url}: {e}")
    except Exception as e:
        print(f"Unexpected error for {post_url}: {e}")
    return {"data": data}


def getPostAttachments(USER_ID, POST_ID, n=1):
    post_url = createPostAttachmentsUrl(USER_ID, POST_ID, APP_ID, APP_SECRET)
    print(f"Fetching attachments for post: {USER_ID}_{POST_ID}")
    print(f"Attachments URL: {post_url}")
    time.sleep(n)
    try:
        web_response = urllib.request.urlopen(post_url)
        readable_page = web_response.read()
        return json.loads(readable_page)
    except urllib.error.HTTPError as e:
        print(f"HTTPError for {post_url}: {e}")
    except urllib.error.URLError as e:
        print(f"URLError for {post_url}: {e}")
    except Exception as e:
        print(f"Unexpected error for {post_url}: {e}")
    return {}


if __name__ == "__main__":
    buzzfeed = []
    n = 20

    outlet_urls = {
        "ABC_News_Politics": 'abc',
        "Addicting_Info": 'addictinginfo',
        "CNN_Politics": "cnn",
        "Eagle_Rising": "eaglerising",
        "Freedom_Daily": "freedomdaily",
        "Occupy_Democrats": "occupydemocrats",
        "Politico": "politi.co",
        "Right_Wing_News": "rightwingnews",
        "The_Other_98%": "TheOther98"
    }

    buzzfeed_file = 'facebook-fact-check.csv'
    with open(buzzfeed_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            buzzfeed.append(row)

    del buzzfeed[0]
    for article in buzzfeed:
        if article:
            USER_ID = article[0]
            POST_ID = article[1]
            outlet = article[3].replace(" ", "_")
            article_type = article[6]

            print(f"Working on post {POST_ID}")
            try:
                time.sleep(n)
                postJson = getPost(USER_ID, POST_ID)
                postJson['type'] = article_type
            except:
                print("Post error")
                postJson = {}

            try:
                commentJson = getPostComments(USER_ID, POST_ID, n)
            except:
                print("Comment error")
                commentJson = {}

            try:
                attachJson = getPostAttachments(USER_ID, POST_ID, n)
            except:
                print("Attachment error")
                attachJson = {}

            post_dir = os.path.join('dataset', outlet, POST_ID)
            os.makedirs(post_dir, exist_ok=True)

            with open(os.path.join(post_dir, 'posts.json'), 'w') as f:
                json.dump(postJson, f, indent=4, sort_keys=True)

            with open(os.path.join(post_dir, 'comments.json'), 'w') as f2:
                json.dump(commentJson, f2, indent=4, sort_keys=True)

            with open(os.path.join(post_dir, 'attach.json'), 'w') as f4:
                json.dump(attachJson, f4, indent=4, sort_keys=True)
