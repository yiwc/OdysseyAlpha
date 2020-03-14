from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

# plt.imshow(data, interpolation='nearest')
# plt.show()
w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
# img = Image.fromarray(data, 'RGB')
# img.save('my.png')
# img.show()
plt.imshow(data)
plt.show()