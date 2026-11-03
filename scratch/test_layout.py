
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon

fig = plt.figure(figsize=(10.5, 15.5), dpi=350)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 150)
ax.axis('off')

print('Test layout script template ready')
