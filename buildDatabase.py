from pathlib import Path
import cv2
import numpy as np

from imageUtils import list_images, load_image, feature_vector, determine_aspect

INPUT_FOLDER = "./snafus"
OUTPUT_FILE = "./cache/imageDatabase.npz"

def normalize(v):
    norm = np.linalg.norm(v)

    if norm == 0:
        return v

    return v / norm

def main():
    Path("./cache").mkdir(exist_ok=True)

    vectors = []
    paths = []
    aspects = []
    widths = []
    heights = []

    files = list_images(INPUT_FOLDER)

    total = len(files)

    for i, file in enumerate(files):
        print(f"[{i+1}/{total}] {file.name}")

        try:
            image = load_image(file)

        except Exception as e:
            print(e)
            continue

        h, w = image.shape[:2]

        vector = feature_vector(image)
        vector = normalize(vector)

        vectors.append(vector.astype(np.float32))
        paths.append(str(file))
        aspects.append(determine_aspect(w, h))
        widths.append(w)
        heights.append(h)

    vectors = np.stack(vectors)

    np.savez_compressed(
        OUTPUT_FILE,
        vectors=vectors,
        paths=np.array(paths),
        aspects=np.array(aspects),
        widths=np.array(widths),
        heights=np.array(heights)
    )
    
    print(f"saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
