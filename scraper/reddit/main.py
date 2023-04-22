import os
import argparse
import praw
import psycopg2
from datetime import datetime
from psycopg2 import Error

# Load Reddit credentials from environment variables
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')

# Load PostgreSQL details from environment variables
POSTGRES_USER = os.environ.get('PGUSER')
POSTGRES_PASSWORD = os.environ.get('PGPASSWORD')
POSTGRES_HOST = os.environ.get('PGHOST')
POSTGRES_PORT = os.environ.get('PGPORT')
POSTGRES_DATABASE = os.environ.get('PGDATABASE')

# Initialize the Reddit API wrapper
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('subreddit', help='The name of the subreddit to scrape')
args = parser.parse_args()

# Connect to PostgreSQL database
def connect():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

# Connect to the PostgreSQL database
def connect():
    return psycopg2.connect(user=POSTGRES_USER,
                                  password=POSTGRES_PASSWORD,
                                  host=POSTGRES_HOST,
                                  port=POSTGRES_PORT,
                                  database=POSTGRES_DATABASE)

# Define the subreddit to scrape
subreddit = reddit.subreddit(args.subreddit)

# Iterate through all the posts in the subreddit
for post in subreddit.new(limit=None):
    created = datetime.fromtimestamp(post.created_utc)

    try:
        # Insert the post data into the database
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO posts (id, title, author, created_utc, num_comments, score, url, text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (post.id, post.title, post.author.name, created, post.num_comments, post.score, post.url, post.selftext))
        connection.commit()
        print("Post inserted successfully")
    except (Exception, Error) as error:
        print("Error while inserting post into PostgreSQL database:", error)

# Close the database connection
cursor.close()
connection.close()
print("PostgreSQL connection is closed")
