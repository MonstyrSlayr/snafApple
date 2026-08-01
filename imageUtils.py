from pathlib import Path

import cv2
import numpy as np

FEATURE_SIZE = 32

ASPECT_SQUARE = "1:1"
ASPECT_WIDE = "16:9"
ASPECT_TALL = "9:16"
ASPECT_43 = "4:3"
ASPECT_34 = "3:4"

def determine_aspect(width: int, height: int) -> str:
    ratio = width / height

    options = {
        ASPECT_SQUARE: 1,
        ASPECT_WIDE: 16 / 9,
        ASPECT_TALL: 9 / 16,
        ASPECT_43: 4 / 3,
        ASPECT_34: 3 / 4,
    }

    return min(options, key=lambda k: abs(options[k] - ratio))

def load_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(f"Could not read image: {path}")

    return image

def resize_and_pad(image, size=FEATURE_SIZE):
    h, w = image.shape[:2]

    scale = min(size / w, size / h)

    nw = int(round(w * scale))
    nh = int(round(h * scale))

    resized = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((size, size, 3), dtype=np.uint8)

    x = (size - nw) // 2
    y = (size - nh) // 2

    canvas[y:y + nh, x:x + nw] = resized

    return canvas

def grayscale_feature(image):
    image = resize_and_pad(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return gray.astype(np.float32) / 255.0

def binary_feature(image):
    gray = grayscale_feature(image)

    binary = (gray > 0.5).astype(np.float32)

    return binary

def edge_feature(image):
    image = resize_and_pad(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(gray, 80, 160)

    return edge.astype(np.float32) / 255.0

def feature_vector(image):
    gray = grayscale_feature(image)
    binary = binary_feature(image)
    edge = edge_feature(image)

    GRAY_WEIGHT = 0.20
    BINARY_WEIGHT = 0.65
    EDGE_WEIGHT = 0.15

    return np.concatenate([
        gray.flatten() * GRAY_WEIGHT,
        binary.flatten() * BINARY_WEIGHT,
        edge.flatten() * EDGE_WEIGHT,
    ])

def resize_for_tile(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def list_images(folder):
    extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp"
    }

    images = []

    for file in sorted(Path(folder).iterdir()):

        if file.suffix.lower() in extensions:
            images.append(file)

    return images
