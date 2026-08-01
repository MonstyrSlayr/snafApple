from dataclasses import dataclass
import csv

@dataclass
class RedditPost:
    id: str
    created_utc: int
    title: str
    selftext: str
    author: str
    subreddit: str
    score: int
    num_comments: int
    url: str
    permalink: str
    domain: str
    post_hint: str
    content_type: str
    is_self: bool
    is_video: bool
    over_18: bool
    spoiler: bool
    locked: bool
    stickied: bool

def str_to_bool(value: str) -> bool:
    return value.lower() == "true"

def load_posts(csv_file: str) -> list[RedditPost]:
    posts = []

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            posts.append(
                RedditPost(
                    id=row["id"],
                    created_utc=int(row["created_utc"] or 0),
                    title=row["title"],
                    selftext=row["selftext"],
                    author=row["author"],
                    subreddit=row["subreddit"],
                    score=int(row["score"] or 0),
                    num_comments=int(row["num_comments"] or 0),
                    url=row["url"],
                    permalink=row["permalink"],
                    domain=row["domain"],
                    post_hint=row["post_hint"],
                    content_type=row["content_type"],
                    is_self=str_to_bool(row["is_self"]),
                    is_video=str_to_bool(row["is_video"]),
                    over_18=str_to_bool(row["over_18"]),
                    spoiler=str_to_bool(row["spoiler"]),
                    locked=str_to_bool(row["locked"]),
                    stickied=str_to_bool(row["stickied"]),
                )
            )

    return posts

posts = load_posts("./redditPosts.csv")
posts.reverse()

if (__name__ == "__main__"):
    print(f"loaded {len(posts)} posts")
    print(posts[0])
