from dataclasses import dataclass
import csv

from filterAllPosts import filtered_posts

usage_stats = []

with open("./usageStats.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        usage_stats.append(row)

for post in filtered_posts:
    post.total_usages = 0

skip_all = False

for frame in usage_stats:
    if skip_all:
        break

    for id_key in frame.keys():
        if id_key == "frame":
            print(frame[id_key])
            continue

        da_post = next((post for post in filtered_posts if post.id == id_key), None)
        
        if da_post == None:
            print("greivous error")
            raise

        da_post.total_usages += int(frame[id_key])

# get total posts used
total_posts_used = 0
authors = set()
author_posts_used = {}
author_total_used = {}

for post in filtered_posts:
    if post.total_usages > 0:
        total_posts_used += 1

        authors.add(post.author)
        author_posts_used[post.author] = author_posts_used.get(post.author, 0) + 1
        author_total_used[post.author] = author_total_used.get(post.author, 0) + post.total_usages

for author in authors:
    author_posts_used[post.author] = author_posts_used.get(post.author, 0)

print("total posts used:", total_posts_used)
print()

LEADERBOARD_SIZE = 10

# get post with most usages
sorted_by_appearance = sorted(filtered_posts, key=lambda post: post.total_usages)

print("most used posts:")

for i in range(LEADERBOARD_SIZE):
    print(str(i + 1) + ":", sorted_by_appearance[len(sorted_by_appearance) - 1 - i].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 1 - i].total_usages)
print()

# most author
author_sort_by_posts = sorted(list(authors), key=lambda author: author_posts_used[author])

print("most used authors:")
for i in range(LEADERBOARD_SIZE):
    print(str(i + 1) + ":", author_sort_by_posts[len(author_sort_by_posts) - 1 - i] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 1 - i]])
print()

author_sort_by_total = sorted(list(authors), key=lambda author: author_total_used[author])

print("most appeared authors:")
for i in range(LEADERBOARD_SIZE):
    print(str(i + 1) + ":", author_sort_by_total[len(author_sort_by_total) - 1 - i] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 1 - i]])
print()

AUTHOR_ANALYSIS = ["MonstyrSlayr", "DaToast815", "CobaltChromeA", "DampButter"]
for author in AUTHOR_ANALYSIS:
    print(author, "usages:", author_posts_used.get(author, 0))
    print(author, "appearances:", author_total_used.get(author, 0))

    author_posts = list(filter(lambda post: post.author == author and post.total_usages >  0, filtered_posts))
    sorted_author_posts = sorted(author_posts, key=lambda post: -post.total_usages)

    print(author, "posts:")
    for post in sorted_author_posts:
        print(post.id + ":", post.total_usages)

    print()
