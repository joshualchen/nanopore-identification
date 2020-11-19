import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

grids = range(17, 25)
radii = range(2, 5)

fs = []

for grid in grids:
    for radius in radii:
        im = Image.open("overlap_plotted_grid_"+str(grid)+"_radius_"+str(radius)+".png")
        fs.append(im)

x, y = fs[0].size

ncol = 8
nrow = 3
cvs = Image.new('RGB',(x*ncol,y*nrow))

for i in range(len(fs)):
    px, py = x*int(i/nrow), y*(i%nrow)
    cvs.paste(fs[i],(px,py))
    
#cvs.show()
cvs1 = cvs.save("fullList_gridPlots.png")
