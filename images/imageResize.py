import cv2

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
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

def insertIntoBlankImage(folder, new_size=(416, 416), invert=False):

    #get all files
    img_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    for file_name in img_files:

        name, extension = os.path.splitext(file_name)

        #Read image
        img = cv2.imread(os.path.join(folder, file_name))
        
        #Get image shape
        (h_img, w_img) = img.shape[:2]

        #New shape component
        h_new = new_size[0]
        w_new = new_size[1]

        #New blank image with new shape 
        img_new = np.zeros([h_new, w_new,3],dtype=np.uint8)
        img_new.fill(255)

        #Insert image in the center of blank image
        img_new[int((h_new-h_img)/2):int((h_new+h_img)/2), int((w_new-w_img)/2):int((w_new+w_img)/2)] = img

        #save
        cv2.imwrite(os.path.join(folder, name + "_resize" + extension ), img_new) 

if __name__ == '__main__':

    #Get argument
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument( "-r", "--folderRoot", required=True, help="Set absolute folder path")
    ap.add_argument( "-n", "--folderName", required=True, choices=["train", "validation"],  help="Chose the type of dataset")
    
     
