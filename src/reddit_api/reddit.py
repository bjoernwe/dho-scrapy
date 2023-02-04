PUBLIC = "3heTn63poakqQLY2FJarag"
SECRET = "N236hpjVEgeyVOphiBeYbZUVYC4RqA"


import requests

auth = requests.auth.HTTPBasicAuth(PUBLIC, SECRET)

subreddit = "streamentry"
url = f"https://oauth.reddit.com/r/{subreddit}/hot"

data = {"grant_type": "password", "username": "CapaceDT", "password": "SiM9y8I#$E1K"}

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
