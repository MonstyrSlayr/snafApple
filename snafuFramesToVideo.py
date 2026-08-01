# converts symbolframes to a video (no sound)

import cv2 as cv
import os

w = 642
h = 480
fps = 29.97

symbolFramesDirectory = os.fsencode("snafuFrames")
symbolFramesCount = sum(1 for _, _, files in os.walk("snafuFrames") for f in files)
frames = [None] * symbolFramesCount

for file in os.listdir(symbolFramesDirectory):
    filenameReal = os.fsdecode(file)
    filename = "./snafuFrames/" + filenameReal
    
    frame = cv.imread(filename, cv.IMREAD_UNCHANGED)
    daIndex = int(filenameReal.replace(".jpg", "").replace("frame", ""))
    frames[daIndex] = frame

print(len(frames))

writer = cv.VideoWriter("videoOutput.mp4", -1, fps, (w, h))

for frame in frames:
    writer.write(frame)

writer.release()
