import csv
import time
import requests

SUBREDDIT = "coaxedintoasnafu"
OUTPUT_FILE = "./redditPosts.csv"

BASE_URL = "https://arctic-shift.photon-reddit.com/api/posts/search"

# in case i wanna do other queries with it i guess
FIELDS = [
    "id",
    "created_utc",
    "title",
    "selftext",
    "author",
    "subreddit",
    "score",
    "num_comments",
    "url",
    "permalink",
    "domain",
    "post_hint",
    "content_type",
    "is_self",
    "is_video",
    "over_18",
    "spoiler",
    "locked",
    "stickied",
]

def content_type(post):
    if post.get("is_self"):
        return "text"

    if post.get("is_video"):
        return "video"

    hint = post.get("post_hint")

    if hint:
        return hint

    return "unknown"

after = None
total = 0

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()

    while True:
        params = {
            "subreddit": SUBREDDIT,
            "limit": 100,
            "sort": "asc"
        }

        if after is not None:
            params["after"] = after

        r = requests.get(BASE_URL, params=params, timeout=60)
        r.raise_for_status()

        data = r.json()

        posts = data.get("data", [])

        if not posts:
            break

        for post in posts:
            writer.writerow({
                "id": post.get("id"),
                "created_utc": post.get("created_utc"),
                "title": post.get("title"),
                "selftext": post.get("selftext"),
                "author": post.get("author"),
                "subreddit": post.get("subreddit"),
                "score": post.get("score"),
                "num_comments": post.get("num_comments"),
                "url": post.get("url"),
                "permalink": "https://reddit.com" + post.get("permalink", ""),
                "domain": post.get("domain"),
                "post_hint": post.get("post_hint"),
                "content_type": content_type(post),
                "is_self": post.get("is_self"),
                "is_video": post.get("is_video"),
                "over_18": post.get("over_18"),
                "spoiler": post.get("spoiler"),
                "locked": post.get("locked"),
                "stickied": post.get("stickied"),
            })

        total += len(posts)
        print(f"downloaded {total:,} posts")

        after = posts[-1]["created_utc"]

        time.sleep(0.5)

print("garbgar")
