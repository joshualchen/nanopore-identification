import os
import os.path
import numpy as np
import matplotlib.pyplot as plt

# basically what i need to do is do a thing for each specific radius


def forRadius(grid, radius):
    data = []  # good
    currentDir = os.getcwd()  # good
    fileNames = []  # good
    for filename in os.listdir(currentDir):
        if filename.startswith('success_'):
            fileNames.append(filename[:-4])
            file_data = []
            file_data_x = []
            file_data_y = []
            f = open(filename, 'r')
            for line in f:
                if len(line.split()) == 4:
                    if line.split()[0] == grid and line.split()[1] == radius:
                        stuff = line.split()
                        file_data_x.append(float(stuff[2]))
                        file_data_y.append(float(stuff[3]))
            file_data.append(file_data_x)
            file_data.append(file_data_y)
            data.append(file_data)

    numberOfFiles = len(fileNames)

    def plotEverything(data, numberOfFiles):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        newColors = []
        minSize = 4
        maxSize = 24
        sizes = []
        for x in range(numberOfFiles):
            newColors.append(colors[x])
        stepSize = (maxSize-minSize) / (numberOfFiles - 1)
        for x in range(numberOfFiles):
            sizes.append(maxSize - x * stepSize)
        for x in range(numberOfFiles):  # numberOfFiles):
            plt.plot(data[x][0], data[x][1], newColors[x]+'o',
                     markersize=sizes[x], label=fileNames[x]+'\n')

    plotEverything(data, numberOfFiles)
    lgd = plt.legend(bbox_to_anchor=(1.04,0.5), loc = 'center left', fontsize=12)
    axes = plt.gca()
    #axes.set_xlim([71.5,77.5])
    #axes.set_ylim([6.5,13.5])
    plt.title('For $\it{grid}$ = '+grid+', $\it{radius}$ = ' + radius, fontsize=16)
    plt.xlabel('$\it{threshold}$ value', fontsize=16)
    plt.ylabel('$\it{area}$ value', fontsize=16)
    plt.savefig('overlap_plotted_grid_'+grid+'_radius_' + radius, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()
    # plt.show()


def forGrid(grid):
    forRadius(grid, "3")
    forRadius(grid, "4")
    forRadius(grid, "5")
    forRadius(grid, "6")
    forRadius(grid, "7")
    forRadius(grid, "8")
    forRadius(grid, "9")
    


forGrid("18")
forGrid("19")
forGrid("20")
forGrid("21")
