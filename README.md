# Sudoku resolver using YOLO v4

The target of this project is to apply YOLO v4 object detection alghorithm in a custom Sudoku resolver.

Given Sudoku input image, the main steps are:

 1) [Configure YOLO v4 to identify numbers and empty cells](#configure-yolo-v4-to-identify-numbers-and-empty-cells);
 2) [Position establishment of numbers and empty cells](#position-establishment-of-number-and-empty-cells);
 3) [Apply a generic alghorithm to resolve the game](#apply-a-generic-alghorithm-to-resolve-the-game)

#### Configure YOLO v4 to identify numbers and empty cells

To achieve this point YOLO v4 has been trained with a dataset of numbers and empty cells.
An example of dataset structure is contained in `dataset` folder. 

Execute: `python3 .\images\imageResize.py -r "dirOfFolder" -n train -s 620`
to create in `dirOfFolder/train` or `dirOfFolder/validation`, different images with size [620, 620] that conatains a number/empty cell image with different scale. Every image is coupled with .txt file with bbox infos.
 
Nex step is execute: 
`python3 .\images\listCreator.py -r "dirOfFolder" -n train --type list`
to create `train.txt` or `validation.txt` that contains a list of all files (need for YOLO v4 training).

The final command:
`python3 .\images\listCreator.py -r "dirOfFolder" -n train --type cfg`
to create all configuration files for YOLO v4:
* obj.name;
* obj-var.out.data;
* yolov4-custom-var-out.cfg.

for more details https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

Now all you need to train YOLO v4 is ready.

Because training phase is boosted up by Google Colab (https://colab.research.google.com/notebooks/intro.ipynb), you need Google Drive.

Create these compressed folder:
* `datset.zip` with training and validation folders;
* `cfg.zip` with the above configuration files.
* upload to Google Drive.

The Google Colab notebook with all command is in `GoogleColab/objectDetection.ipynb`.

For more details on YOLO v4 watch on https://github.com/AlexeyAB/darknet#pre-trained-models.

#### Position establishment of numbers and empty cells 

After a sufficient network training, the next step is to identify in the Sudoku image the position of numbers and those of empty cells.
For this purpose i used python openCV (at least 4.4.0) in which is integrated the use of YOLO v4 network. 
For this purpose a sliding window of dimension [72,72] is used (centerd in 9 * 9, vetical * horizontal points) in which apply YOLO v4 trained network to identify numbers or empty cells.
The info of positon and the type of objects are stored in matrix array.
All details are contained in `pythonYolo/yolo.py`

#### Apply a generic alghorithm to resolve the game
From this matrix i applied a generic Sudoku resolver to obtain the solution (https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/)
After, the result numbers (in `number` folder) are pasted in the original image.

## Pick all together and test the application
With `python3 .\pythonYolo\yolo.py -i sudokuImgToDetect -y folderOfCfgFiles` you can test the application.
Some codes line are taken from (https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)

## Result
![sudoku_result](https://github.com/gaggioma/ObjectDetection/blob/master/img/res.jpg)

## Further development
* identifing Sudoku image inside a mixed image. This is make possibile adding a YOLO v4 block before processing phase;
* triain YOLO v4 with a more accurate and numerous training set.