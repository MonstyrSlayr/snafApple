# simply converts a video to frames
# change leading zeros if necessary

import cv2

vidcap = cv2.VideoCapture("./badApple360.mp4")
success,image = vidcap.read()
count = 0
while success:
    cv2.imwrite("frames/frame%04d.jpg" % count, image)
    success,image = vidcap.read()
    count += 1
