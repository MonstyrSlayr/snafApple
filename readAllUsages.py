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

print("total posts used:", total_posts_used)
print()

# get post with most usages
sorted_by_appearance = sorted(filtered_posts, key=lambda post: post.total_usages)

print("most used posts:")
print(sorted_by_appearance[len(sorted_by_appearance) - 1].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 1].total_usages)
print(sorted_by_appearance[len(sorted_by_appearance) - 2].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 2].total_usages)
print(sorted_by_appearance[len(sorted_by_appearance) - 3].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 3].total_usages)
print(sorted_by_appearance[len(sorted_by_appearance) - 4].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 4].total_usages)
print(sorted_by_appearance[len(sorted_by_appearance) - 5].id + ":", sorted_by_appearance[len(sorted_by_appearance) - 5].total_usages)
print()

# most author
author_sort_by_posts = sorted(list(authors), key=lambda author: author_posts_used[author])

print("most used authors:")
print(author_sort_by_posts[len(author_sort_by_posts) - 1] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 1]])
print(author_sort_by_posts[len(author_sort_by_posts) - 2] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 2]])
print(author_sort_by_posts[len(author_sort_by_posts) - 3] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 3]])
print(author_sort_by_posts[len(author_sort_by_posts) - 4] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 4]])
print(author_sort_by_posts[len(author_sort_by_posts) - 5] + ":", author_posts_used[author_sort_by_posts[len(author_sort_by_posts) - 5]])
print()

author_sort_by_total = sorted(list(authors), key=lambda author: author_total_used[author])

print("most appeared authors:")
print(author_sort_by_total[len(author_sort_by_total) - 1] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 1]])
print(author_sort_by_total[len(author_sort_by_total) - 2] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 2]])
print(author_sort_by_total[len(author_sort_by_total) - 3] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 3]])
print(author_sort_by_total[len(author_sort_by_total) - 4] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 4]])
print(author_sort_by_total[len(author_sort_by_total) - 5] + ":", author_total_used[author_sort_by_total[len(author_sort_by_total) - 5]])
print()
