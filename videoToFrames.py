# simply converts a video to frames
# change leading zeros if necessary

import cv2
from pathlib import Path

vidcap = cv2.VideoCapture("./badApple480.mp4")
success,image = vidcap.read()
count = 0
Path("./frames").mkdir(exist_ok=True)
while success:
    print(count)
    cv2.imwrite("./frames/frame%04d.jpg" % count, image)
    success,image = vidcap.read()
    count += 1
