import argparse
import os

import pathlib

import cv2

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

def createBBox(rootFolder, name):

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
                file.write(folderName + " " + str(0.5) + " " + str(0.5) + " " + str(1) + " " + str(1) )
                file.close()

if __name__ == '__main__':

    #Get argument
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument( "-n", "--folderName", required=True, choices=["train", "validation"],  help="Chose the type of dataset")
    ap.add_argument( "-b", "--boundingBox", required=True, choices=["yes", "no"],  help="Chose if create bounding box")

    args = vars(ap.parse_args())
    name = args["folderName"]
    bbox = args["boundingBox"]

    #Script folder
    rootFolder = os.path.join(pathlib.Path(__file__).parent.absolute(), name) #os.path.join(".", "OID", "Dataset", name)

    if bbox == "no":
        createList(rootFolder, name)
    elif bbox == "yes" :
        createBBox(rootFolder, name)

    print("complete!!")