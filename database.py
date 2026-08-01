from pathlib import Path

import cv2
import numpy as np

from imageUtils import feature_vector, determine_aspect

try:
    import cupy as cp

    xp = cp
    GPU_ENABLED = True

    print("using CuPy GPU acceleration")

except ImportError:
    xp = np
    GPU_ENABLED = False

    print("using NumPy CPU acceleration")

class ImageDatabase:
    def __init__(self, database_file):
        data = np.load(database_file, allow_pickle=True)

        self.paths = data["paths"]
        self.aspects = data["aspects"]

        vectors = data["vectors"].astype(np.float32)

        if GPU_ENABLED:
            self.vectors = cp.asarray(vectors)
        else:
            self.vectors = vectors

        # store indexes by aspect ratio

        self.aspectIndices = {}

        for i, aspect in enumerate(self.aspects):
            if aspect not in self.aspectIndices:
                self.aspectIndices[aspect] = []

            self.aspectIndices[aspect].append(i)

        for aspect in self.aspectIndices:
            indexes = np.array(self.aspectIndices[aspect], dtype=np.int32)

            if GPU_ENABLED:
                indexes = cp.asarray(indexes)

            self.aspectIndices[aspect] = indexes

        self.imageCache = {}

    def normalize(self, vector):

        length = np.linalg.norm(vector)

        if length == 0:
            return vector

        return vector / length

    def getAspectCandidates(self, aspect):
        return self.aspectIndices.get(aspect, [])

    def matchTile(self, tile, usageCounts):
        h, w = tile.shape[:2]

        aspect = determine_aspect(w, h)

        vector = feature_vector(tile)

        vector = self.normalize(vector)

        if GPU_ENABLED:
            vector = cp.asarray(vector)

        indexes = self.aspectIndices[aspect]

        candidates = self.vectors[indexes]

        scores = candidates @ vector

        for i, databaseIndex in enumerate(indexes):
            penalty = usageCounts.get(self.getFilename(int(databaseIndex)), 0)
            scores[i] -= penalty * 0.03

        bestPosition = int(xp.argmax(scores))

        score = scores[bestPosition]

        if GPU_ENABLED:
            score = float(cp.asnumpy(score))

            bestIndex = int(cp.asnumpy(indexes[bestPosition]))

        else:
            score = float(score)

            bestIndex = int(indexes[bestPosition])

        return bestIndex, score

    def findBest(self, tile, usageCounts):
        index, score = self.matchTile(tile, usageCounts)

        return (
            self.getImage(index),
            score,
            self.getFilename(index)
        )

    def getFilename(self, index):
        return Path(self.paths[index]).stem

    def getImage(self, index):
        if index in self.imageCache:
            return self.imageCache[index]

        image = cv2.imread(self.paths[index], cv2.IMREAD_COLOR)

        # smart
        self.imageCache[index] = image
        return image
