import requests

from settings import ScrapySettings

settings = ScrapySettings()

auth = requests.auth.HTTPBasicAuth(settings.reddit_public_id, settings.reddit_secret)

subreddit = "streamentry"
url = f"https://oauth.reddit.com/r/{subreddit}/hot"

data = {
    "grant_type": "password",
    "username": settings.reddit_username,
    "password": settings.reddit_password,
}

headers = {"User-Agent": "MyAPI/0.0.1"}

res = requests.post(
    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers
)

TOKEN = res.json()["access_token"]

headers["Authorization"] = f"bearer {TOKEN}"

requests.get("https://oauth.reddit.com/api/v1/me", headers=headers).json()
response = requests.get(url, headers=headers)
data = response.json()

# Get the top 10 hot threads
threads = data["data"]["children"][:10]

# Print the title and score of each thread
for thread in threads:
    title = thread["data"]["title"]
    score = thread["data"]["score"]
    print(f"{title}: {score}")
#
