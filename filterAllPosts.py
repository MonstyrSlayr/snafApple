import re
import os
from urllib.parse import urlparse
import requests

from readAllPosts import posts

# filter posts: only sfw posts with at least 1k score and an image, existing accounts only and the image is hosted on reddit.com
filtered_posts = []
for post in posts:
    if post.score < 1000:
        continue

    if post.content_type != "image":
        continue

    if post.over_18:
        continue

    if post.author == "[deleted]":
        continue

    if post.domain != "i.redd.it" and post.domain != "reddit.com":
        continue

    filtered_posts.append(post)

print(f"{len(filtered_posts)} filtered posts")

def download_image(name: str, image_url: str, directory: str) -> str:
    """
    Downloads an image to the specified directory.

    Args:
        name: Name to save the file as (without extension).
        image_url: URL of the image.
        directory: Directory to save the image in.

    Returns:
        The full path to the downloaded image.

    Raises:
        requests.HTTPError: If the download fails.
    """

    os.makedirs(directory, exist_ok=True)

    response = requests.get(
        image_url,
        stream=True,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )
    response.raise_for_status()

    # Determine file extension
    path = urlparse(image_url).path
    extension = os.path.splitext(path)[1]

    if not extension:
        content_type = response.headers.get("Content-Type", "")
        if "png" in content_type:
            extension = ".png"
        elif "gif" in content_type:
            extension = ".gif"
        elif "webp" in content_type:
            extension = ".webp"
        else:
            extension = ".jpg"

    filename = f"{name}{extension}"
    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)

    return filepath

if __name__ == "__main__":
    i = 0
    for post in filtered_posts:
        print(f"downloading {i}: {post.title}")
        name = post.title.replace(" ", "_")
        clean_name = re.sub(r"[^a-zA-Z0-9_]", "", name)

        try:
            download_image(f"{post.id}", post.url, "./snafus")
            i += 1
        except requests.exceptions.HTTPError:
            print("image probably doesn't exist")

    print("jaundice")
