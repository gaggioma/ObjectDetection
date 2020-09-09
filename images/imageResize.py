import argparse
import os
import pathlib
import cv2
import numpy as np

def image_resize(imagePath, width = None, height = None, inter = cv2.INTER_AREA):

    #Read img
    image = cv2.imread(imagePath)

    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def insertIntoBlankImage(rawimg, new_size=(512, 512), invert=False):

    #get all files
    #img_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    #for file_name in img_files:

    #name, extension = os.path.splitext(file_name)

    #Read image
    #img = cv2.imread(os.path.join(folder, file_name))
    
    #Get image shape
    (h_img, w_img) = rawimg.shape[:2]

    #New shape component
    h_new = new_size[0]
    w_new = new_size[1]

    #New blank image with new shape 
    img_new = np.zeros([h_new, w_new,3],dtype=np.uint8)
    img_new.fill(255)

    #Insert image in the center of blank image
    if h_new >= h_img and w_new >= w_img:
        img_new[int((h_new-h_img)/2):int((h_new+h_img)/2), int((w_new-w_img)/2):int((w_new+w_img)/2)] = rawimg
    else:
        print("Resized image too large")
        print("Original (h, w)= (" + str(h_img) + ", " + str(w_img) + ")")
        print("New (h, w)= (" + str(h_new) + ", " + str(w_new) + ")")
        return []

    return img_new

    #save
    #cv2.imwrite(os.path.join(folder, name + "_resize" + extension ), img_new) 

if __name__ == '__main__':

    #Get argument
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument( "-r", "--folderRoot", required=True, help="Set absolute folder path")
    ap.add_argument( "-n", "--folderName", required=True, choices=["train", "validation"],  help="Chose the type of dataset")

    #Vector of width rescalling image
    basewidth = [28, 56, 112, 224, 392]

    args = vars(ap.parse_args())
    pathSource = args["folderRoot"]
    folderName = args["folderName"]

    
    
    #Get all folders in folderRoot/name
    folderList = [name for name in os.listdir(os.path.join(pathSource, folderName)) if os.path.isdir(os.path.join(pathSource, folderName, name)) ]
    folderCount = 0
    for folder in folderList:

        print("processing folder: " + folder)

        #for each file
        fileList = [name for name in os.listdir(os.path.join(pathSource, folderName, folder)) if os.path.isfile(os.path.join(pathSource, folderName, folder, name)) ]

        #Remove all resized file
        for file_name in  fileList:
            name, extension = os.path.splitext(file_name)
            if "resized" in name:
                os.remove(os.path.join(pathSource, folderName, folder, file_name))

        fileList = [name for name in os.listdir(os.path.join(pathSource, folderName, folder)) if os.path.isfile(os.path.join(pathSource, folderName, folder, name)) ]
        for file_name in fileList:

            name, extension = os.path.splitext(file_name)

            #Remove txt file
            if extension == ".txt":
                os.remove(os.path.join(pathSource, folderName, folder, file_name))
                continue

            #Resize for each value in basewidth
            fileNameComplete = os.path.join(pathSource, folderName, folder, file_name)
            for width in basewidth:

                #Resize img
                img_resized = image_resize(fileNameComplete, width)        

                #Insert into black image
                img_new = insertIntoBlankImage(img_resized)

                if len(img_new) != 0:

                    #Save new file
                    cv2.imwrite(os.path.join(pathSource, folderName, folder, name + "_resized_" + str(width) + extension), img_new)
                    (h_resized, w_resized) = img_resized.shape[:2]
                    (h_new, w_new) = img_new.shape[:2]
                    #bbox file
                    file = open(os.path.join(pathSource, folderName, folder, name + "_resized_" + str(width) + ".txt"), 'w')
                    #Write <classname> <x_center> <y_center> <width> <height>
                    file.write(str(folderCount) + " " + str(0.5) + " " + str(0.5) + " " + str(w_resized/w_new) + " " + str(h_resized/h_new) )
                    file.close()

            #Remove origianl file
            os.remove(os.path.join(pathSource, folderName, folder, file_name))
            
        folderCount = folderCount + 1

    print("complete!!")


     
