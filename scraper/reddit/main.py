import os
import argparse
import requests
import psycopg2
from datetime import datetime
from psycopg2 import Error

# Load Pushshift API base URL from environment variables
PUSHSHIFT_API_URL = "https://api.pushshift.io/reddit/search/submission/"

# Load PostgreSQL details from environment variables
POSTGRES_USER = os.environ.get('PGUSER')
POSTGRES_PASSWORD = os.environ.get('PGPASSWORD')
POSTGRES_HOST = os.environ.get('PGHOST')
POSTGRES_PORT = os.environ.get('PGPORT')
POSTGRES_DATABASE = os.environ.get('PGDATABASE')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('subreddit', help='The name of the subreddit to scrape')
args = parser.parse_args()

# Connect to PostgreSQL database
def connect():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def retrieve_min_created(subreddit):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT MIN(created_utc) from posts WHERE subreddit = %s;", (subreddit,))
    min_created_utc = cursor.fetchone()[0]
    connection.close()
    return min_created_utc

def get_posts(subreddit, limit=None, before=None):
    params = {
        "subreddit": subreddit,
        "size": limit or 100,
        "sort_type": "created_utc"
    }
    if before is not None:
        print(before)
        ago = datetime.now() - before
        params["before"] = "%ds" % (ago.total_seconds() + 1)
    response = requests.get(PUSHSHIFT_API_URL, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error {response.status_code} while fetching from Pushshift API")
        print(response.json())
        return []

# Define the subreddit to scrape
subreddit = args.subreddit

def get_next_posts():
    # Retrieve min created_utc for the given subreddit from postgres
    min_created_utc = retrieve_min_created(subreddit)

    # Get the posts from the Pushshift API
    posts = get_posts(subreddit, before=min_created_utc)
    if len(posts) == 0:
        return False

    # Iterate through all the posts in the subreddit
    for post in posts:
        created = datetime.fromtimestamp(post["created_utc"])

        try:
            # Insert the post data into the database
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO posts (id, subreddit, title, author, created_utc, num_comments, score, url, text)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (post["id"], subreddit, post["title"], post["author"], created, post["num_comments"], post["score"], post["url"], post["selftext"]))
            connection.commit()
        except (Exception, Error) as error:
            print("Error while inserting post into PostgreSQL database:", error)
    return True

while True:
    print("getting next batch...")
    some_left = True
    try:
        some_left = get_next_posts()
    except Exception as error:
        print("error getting batch")
    if not some_left:
        break

print("done!")
