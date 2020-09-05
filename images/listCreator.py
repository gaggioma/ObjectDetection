import argparse
import os

import pathlib

import cv2
from shutil import copyfile, rmtree

def createList(rootFolder, name):

    #Remove list.txt if exists
    if(os.path.exists(os.path.join(rootFolder, name + ".txt"))):
        os.remove(os.path.join(rootFolder, name + ".txt"))
    
    #Create list.txt
    file = open(os.path.join(rootFolder, name + ".txt"), 'w')

    #Get all folder inside rootFolder
    folderList = [name for name in os.listdir(rootFolder) if os.path.isdir(os.path.join(rootFolder, name)) ]

    for folderName in folderList:

        filePath = os.path.join(rootFolder, folderName)
        #Get all files
        onlyfiles = [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]

        #Write file path ony for jpeg files
        for singlefile in onlyfiles:
            filename, file_extension = os.path.splitext(singlefile)
            if file_extension == ".jpg":
                file.write("data" + "/" + name + "/" + folderName + "/" + filename + file_extension + "\n")

    file.close()

def createBBox(rootFolder):

    #Get all folder in rootFolder
    folderList = [name for name in os.listdir(rootFolder) if os.path.isdir(os.path.join(rootFolder, name)) ]

    #for each folder
    for folderName in folderList:

        folderPath = os.path.join(rootFolder, folderName)
        fileList = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]

        print("Analize folder: " + folderName)

        #for each image into folder
        for fileImg in fileList:

            filename, file_extension = os.path.splitext(fileImg)

            #delete .txt
            if file_extension == ".txt":
                os.remove(os.path.join(folderPath, fileImg))
            else:
                #Img.txt
                file = open(os.path.join(folderPath, filename + ".txt"), 'w')
                #Write <classname> <x_center> <y_center> <width> <height>
                file.write(folderName + " " + str(0.5) + " " + str(0.5) + " " + str(1.0) + " " + str(1.0) )
                file.close()

def createCfg(rootFolder, cfgFile):

    #read .cfg file vith variables
    cfg = open(cfgFile, "rt")
    cfgData = cfg.read()
    cfg.close()

    #Create new .cfg file
    cfgName, cfg_file_extension = os.path.splitext(os.path.basename(cfgFile))
    cfgOut = open(os.path.join(rootFolder, cfgName + "-out" + ".cfg"), "wt")

    #file with classes list
    classesFile = open(os.path.join(rootFolder, "obj.names"), "wt")

    #Get all folder in rootFolder
    folderList = [name for name in os.listdir(rootFolder) if os.path.isdir(os.path.join(rootFolder, name)) ]

    #for each folder
    counter = 0
    classesNum = 0
    for folderName in folderList:

        #Write class in obj.class
        classesNum = classesNum + 1
        classesFile.write(folderName + "\n")

        folderPath = os.path.join(rootFolder, folderName)
        fileList = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]

        print("Analize folder: " + folderName)

        #for each image into folder
        for fileImg in fileList:

            filename, file_extension = os.path.splitext(fileImg)

            #delete .txt
            if file_extension != ".txt":
                counter = counter + 1

    #Batch size and steps val
    batches_size = counter
    if classesNum * 2000 > counter:
        batches_size = classesNum * 2000

    if batches_size > 6000:
        cfgData = cfgData.replace('max_batches_val', str(batches_size))
        cfgData = cfgData.replace('steps_val', str(round(0.8*batches_size)) + "," + str(round(0.9*batches_size)))

    else:
        cfgData = cfgData.replace('max_batches_val', 6000)
        cfgData = cfgData.replace('steps_val', str(round(0.8*6000)) + "," + str(round(0.9*6000)))
    
    #filters=(classes + 5)x3 in the 3
    if classesNum == 1:
        cfgData = cfgData.replace('filters_val', 18)
    elif classesNum == 2:
        cfgData = cfgData.replace('filters_val', 21)
    else:
        cfgData = cfgData.replace('filters_val', str((classesNum + 5)*3))

    #Classes
    cfgData = cfgData.replace('classes_val', str(classesNum))

    #.data file
    dataFile = open("images\\obj-var.data", "rt")
    dataStr = dataFile.read()
    dataFile.close()
    dataStr = dataStr.replace("classes_val", str(classesNum))
    dataName, data_file_extension = os.path.splitext(os.path.basename("images\\obj-var.data"))
    dataOut = open(os.path.join(rootFolder, dataName + "-out" + data_file_extension), "wt")
    dataOut.write(dataStr)
    dataOut.close()

    #Write in cfgOut
    cfgOut.write(cfgData)
    cfgOut.close()

    classesFile.close()

def copy(pathSource, pathTarget, count):

    #Remove all folders in target and re create
    if os.path.exists(pathTarget):
        rmtree(pathTarget)
    os.mkdir(pathTarget)

    #Create target folder like in source
    folderList = [name for name in os.listdir(pathSource) if os.path.isdir(os.path.join(pathSource, name)) ]
    for folderName in folderList:
        os.mkdir(os.path.join(pathTarget, folderName))

    #copy element [1, count] from source to target
    for folderName in folderList:
        print("Creating " + str(count) + " files in " + folderName)
        folderPath = os.path.join(pathSource, folderName)
        fileListSource = [name for name in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, name))]
        fileCount = 0
        for fileSource in fileListSource:

            #Process only .jpg files
            filename, file_extension = os.path.splitext(fileSource)

            if file_extension == ".jpg":
            
                #Copy file form source to target
                copyfile(os.path.join(pathSource, folderName, fileSource), os.path.join(pathTarget, folderName, fileSource))
                fileCount = fileCount + 1
                if fileCount == count:
                    break
           


if __name__ == '__main__':

    #Get argument
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument( "-r", "--folderRoot", required=True, help="Set absolute folder path")
    ap.add_argument( "-n", "--folderName", required=True, choices=["train", "validation"],  help="Chose the type of dataset")
    ap.add_argument( "-t", "--type", required=True, choices=["list", "bbox", "cfg", "cutImages"],  help="Choose type of elaboration")

    args = vars(ap.parse_args())
    name = args["folderName"]
    typeVar = args["type"]

    #Script folder
    rootFolder = os.path.join(args["folderRoot"], name) #os.path.join(pathlib.Path(__file__).parent.absolute(), name)
    print(pathlib.Path(__file__).parent.absolute())

    if typeVar == "list":
        createList(rootFolder, name)
    elif typeVar == "bbox" :
        createBBox(rootFolder)
    elif typeVar == "cfg":
        createCfg(rootFolder, "images\\yolov4-custom-var.cfg")
    elif typeVar == "cutImages":
        copy(rootFolder, os.path.join(args["folderRoot"], "myImages" , name), 100)

    print("complete!!")