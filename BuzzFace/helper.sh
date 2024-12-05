#!/bin/bash

# Collect the posts, attachments, and top-level comments
echo "Running collectPosts.py..."
python collectPosts.py $1 $2
echo "Finished collectPosts.py"

# Go through and query each top-level comment for their replies, sort them
# and add the appropriate fields
echo "Running threaded_comments.py..."
python threaded_comments.py $1 $2
echo "Finished threaded_comments.py"

# Access the news articles themselves and download the relevant data.
# Also collect the Facebook Plugin and Disqus Plugin comments.
echo "Running scrape.py..."
python scrape.py $1 $2 $3 $4
echo "Finished scrape.py"

# Get the post times and store them for getting response times
echo "Running get_post_times.py..."
python get_post_times.py
echo "Finished get_post_times.py"

# Create the THREADS.json file, the comments organized by thread ID
echo "Running order_by_thread.py..."
python order_by_thread.py
echo "Finished order_by_thread.py"

# Create the USERS.json file, the comments organized by anonymized user ID
echo "Running order_by_user.py..."
python order_by_user.py
echo "Finished order_by_user.py"
