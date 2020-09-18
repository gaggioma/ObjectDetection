# ObjectDetection

The target of this project is to apply yolov4 object detection alghorithm in a custom Sudoku resolver.
In particular, from a given input image (in this first phase the image has the dimension of Sudoku), the main steps to achieve this target are:

 1) identify numbers and empty cells;
 2) apply a generic alghorithm to resolve the game.

Now i analyze in detail this two steps.

To achive 1) yoloV4 has been trained with a dataset of numbers and empty cells.
Follow the command inside command.bat.
In details:
python3 .\imageResize.py -r "dirOfFolder" -n train -s 620
create in dirOfFolder/train different image with size [620,620] in which is pasted a number image with different scale. Every image are coupled with .txt file with bbox infos.
 
with:
python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\EmptyDataset" -n train --type list
create train.txt with the list of all data (need for yolov4 training)

the filna command:
python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\EmptyDataset" -n train --type cfg
create all configuration file for  yoloV4:
obj.name
obj-var.out.data
yolov4-custom-var-out.cfg

Now all you need to trainig yoloV4 is ready.
Create these compressed folder:
datset.zip with training and validation folder;
cfg.zip with the above confuration files.

Trainig phase is boosted up by Google Colab (https://colab.research.google.com/notebooks/intro.ipynb), so upload the previous copressed folder into you Google Drive.

The GoogleColab notebook with all command is in

However more details on yoloV4 is on https://github.com/AlexeyAB/darknet#pre-trained-models 

After a sufficient network trainig the next step is to identify in the sudoku image the position of numbers and empty cells.
For this purpose i used python openCV (at least 4.4.0) in which is integrated the use of yoloV4 network. 
From the original imges i use a sliding window af dimension [72,72] in which apply YoloV4 trained network to identify numbers and empty cells. This infos with the windows position are stored in memory matrix array.

From this matrix i apply a generic sudoku resolver to obtain the solution (https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/)

After thant the result numbers are pasted in the oiginal image.
You can find all this procedure in yolo.py. Some code are taken from (https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)

Furher development:
-before process image create a block to identify a sudoku image.
