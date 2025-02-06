import sys

import numpy as np
np.set_printoptions(sys.maxsize)
# Load the .npz file; allow_pickle is needed if you stored objects (usually not for arrays)
data = np.load("/episodes/ep_1738873272.1680288.npz", allow_pickle=True)

# Access the arrays by their keys (as defined when saving)
frames = data["frames"]  # This will be your (n, 160, 256) array of images
keys = data["keys"]      # This will be your (n, 4) or (n, 5) array of key states
for x in frames:
    print(x)
for x in range(10):
    print("\n")

print("Keys shape:", keys)
