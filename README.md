# nanopore-identification
Autonomously identify nanopores in AC-TEM images of 2D materials by manually labelling a few sample images. Consists of a codebase for a manual grid search and automated comparison, as well as a gradient ascent method to optimize hyperparameters.

# How to use? [Grid search]
1. Label 5-6 sample images that encompass the full set of images that are to be processed by manually filling in pixels using green (rgb: (0, 255, 0)).
2. Run the scripts in succession: 1_testrange8.py, 2_autoOverlap.py, 3_plotOverlap.py. 
3. View the plots produced and choose the parameter combination that best identifies nanopores in the 5-6 sample images. 
