import matplotlib.pyplot as plt
import numpy as np

image = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

fig, ax = plt.subplots()

ax.imshow(image, origin="lower")

plt.show()
