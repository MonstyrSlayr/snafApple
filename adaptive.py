from dataclasses import dataclass
import cv2
import numpy as np


@dataclass
class Tile:
    x: int
    y: int
    w: int
    h: int
    aspect: str


# minimum tile size in pixels
MIN_SIZE = 32

# if a region is "simple enough", stop subdividing
VARIANCE_THRESHOLD = 600

def closest_aspect(w, h):
    ratio = w / h

    choices = {
        "1:1": 1.0,
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "4:3": 4 / 3,
        "3:4": 3 / 4,
    }

    return min(choices, key=lambda k: abs(choices[k] - ratio))

def region_complexity(gray):
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1)

    return np.mean(gx * gx + gy * gy)

def subdivide(gray, x, y, w, h): # recursive
    region = gray[y:y+h, x:x+w]

    complexity = region_complexity(region)

    if (
        complexity < VARIANCE_THRESHOLD
        or w <= MIN_SIZE
        or h <= MIN_SIZE
    ):

        return [Tile(x, y, w, h, closest_aspect(w, h))]

    tiles = []

    # prefer splitting along the longest axis
    if w > h:
        half = w // 2

        tiles.extend(subdivide(gray, x, y, half, h))
        tiles.extend(subdivide(gray, x + half, y, w - half, h))

    else:
        half = h // 2

        tiles.extend(subdivide(gray, x, y, w, half))

        tiles.extend(subdivide(gray, x, y + half, w, h - half))

    return tiles

def generate_tiles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return subdivide(gray, 0, 0, frame.shape[1], frame.shape[0])
