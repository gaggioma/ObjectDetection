import argparse
import os

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


if __name__ == '__main__':

    #Get argument
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument( "-n", "--folderName", required=True, choices=["train", "validation"],  help="Chose the type of dataset")

    args = vars(ap.parse_args())
    name = args["folderName"]

    rootFolder = os.path.join(".", "OID", "Dataset", name)

    createList(rootFolder, name)

    print("complete!!")