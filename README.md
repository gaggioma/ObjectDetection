# Sudoku resolver using YOLO v4

The target of this project is to apply yolo v4 object detection alghorithm in a custom Sudoku resolver.

Given Sudoku input image, the main steps to achieve this target are:

 1) create a network to identify numbers and empty cells;
 2) establish the position of number and empty cells;
 3) apply a generic alghorithm to resolve the game.

Now i analyze in detail this two steps.

#### Identify numbers and empty cells

To achive this point YOLO v4 has been trained with a dataset of numbers and empty cells.
An example of dataset structure is contained in dataset folder. 

Execute: `python3 .\imageResize.py -r "dirOfFolder" -n train -s 620`
to create in dirOfFolder/train or validation, different images with size [620, 620] in which a number image with different scale is pasted. Every image is coupled with .txt file with bbox infos.
 
Nex step is execute: 
`python3 .\listCreator.py -r "dirOfFolder" -n train --type list`
to create train.txt or validation.txt with the list of all data (need for YOLO v4 training).

The final command:
`python3 .\listCreator.py -r "dirOfFolder" -n train --type cfg`
to create all configuration file for YOLO v4:
* obj.name;
* obj-var.out.data;
* yolov4-custom-var-out.cfg

Now all you need to train YOLO v4 is ready.

Because rainig phase is boosted up by Google Colab (https://colab.research.google.com/notebooks/intro.ipynb), you need to upload on you Google Drive.
Create these compressed folder:
* datset.zip with training and validation folder;
* cfg.zip with the above confuration files.
* upload to Google Drive.

The GoogleColab notebook with all command is in `GoogleColab/objectDetection.ipynb`.

For more details on YOLO v4 watch on https://github.com/AlexeyAB/darknet#pre-trained-models.

#### Establish the position of number and empty cells 

After a sufficient network trainig, the next step is to identify in the Sudoku image the position of numbers and empty cells.
For this purpose i used python openCV (at least 4.4.0) in which is integrated the use of YOLO v4 network. 
From the original imges i used a sliding window of dimension [72,72] (centerd in 9 * 9 vetical * horizontal points) in which apply YOLO v4 trained network to identify numbers or empty cells.
The info of positon and the type of objects are stored in matrix array.

#### Apply a generic alghorithm to resolve the game
From this matrix i apply a generic Sudoku resolver to obtain the solution (https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/)
After that the result numbers are pasted in the oiginal image.

You can find all this procedure in yolo.py. Some code are taken from (https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)

Furher development:
-before process image create a block to identify a sudoku image.
