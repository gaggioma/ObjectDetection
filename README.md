# ObjectDetection

The target of this project is to apply yolov4 object detection alghorithm in a concrete way.
My idea is to implent my Sudoku solver using this artificial intelligence algorithm.

Main steps to resolve a Sudoku:
 1) Given a Sudoku genric image, identify numbers and empty cells;
 2) From the matrix contains all values apply a generic alghorithm to resolve the game.

Now i analyze separately this 2 steps.

Given a Sudoku image, identify number and empty cells;

YoloV4 has been trained with a dataset of numbers and empty cells.
In "images" the is all you need to create a sufficient trainig set whith all files need for Yolov4 trainig.

For more details for training https://github.com/AlexeyAB/darknet#pre-trained-models 
Trainig phase is boosted up by Google Colab (https://colab.research.google.com/notebooks/intro.ipynb)
 
From tho original imges i use a sliding window af dimension [72,72] in which apply YoloV4 to identify numbers and empty cells that are stored in in memory matrix array.

From this matrix i apply a generic sudoku resolver to obtain the solution https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/

The resut numbers are paste in the oiginal image.

