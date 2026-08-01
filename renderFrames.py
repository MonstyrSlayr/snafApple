from pathlib import Path
import cv2
from tqdm import tqdm
import csv

from database import ImageDatabase
from adaptive import generate_tiles

FRAME_FOLDER = "./frames"
OUTPUT_FOLDER = "./snafuFrames"
DATABASE_FILE = "./cache/imageDatabase.npz"

def fit_image(image, width, height):
    h, w = image.shape[:2]

    scale = max(width / w, height / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # center crop
    x = (new_w - width) // 2
    y = (new_h - height) // 2

    return resized[y:y + height, x:x + width]

def render_frame(frame, database):
    usageCounts = {}
    output = frame.copy()

    tiles = generate_tiles(frame)

    for tile in tiles:
        crop = frame[
            tile.y:tile.y + tile.h,
            tile.x:tile.x + tile.w
        ]

        image, score, filename = database.findBest(crop, usageCounts)
        usageCounts[filename] = usageCounts.get(filename, 0) + 1

        image = fit_image(image, tile.w, tile.h)

        output[
            tile.y:tile.y + tile.h,
            tile.x:tile.x + tile.w
        ] = image

    return output, usageCounts

def main():
    max_frames = 9999
    i = 0

    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
    database = ImageDatabase(DATABASE_FILE)

    frames = sorted(Path(FRAME_FOLDER).iterdir())
    frames = [
        f for f in frames
        if f.suffix.lower()
        in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        }
    ]

    usageStats = []

    for frame_path in tqdm(frames):
        frame = cv2.imread(str(frame_path))

        if frame is None:
            continue

        result, usageCounts = render_frame(frame, database)
        output_path = (Path(OUTPUT_FOLDER) / frame_path.name)
        cv2.imwrite(str(output_path), result)

        usageStats.append(usageCounts)

        i += 1
        if i >= max_frames:
            break
    
    csv_path = "./usageStats.csv"

    # find every image name that appeared at least once
    all_images = sorted({
        image
        for frame in usageStats
        for image in frame.keys()
    })

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["frame"] + all_images)

        # one row per frame
        for frame_number, frame_usage in enumerate(usageStats):
            row = [frame_number]

            for image in all_images:
                row.append(frame_usage.get(image, 0))

            writer.writerow(row)

    print(f"saved usage statistics to {csv_path}")

if __name__ == "__main__":
    main()
