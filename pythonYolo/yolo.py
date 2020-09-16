# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os

def bk():

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,	help="path to input image")
	ap.add_argument("-y", "--yolo", required=True,	help="base path to YOLO directory")
	ap.add_argument("-c", "--confidence", type=float, default=0.01,	help="minimum probability to filter weak detections")
	ap.add_argument("-t", "--threshold", type=float, default=0.3,	help="threshold when applying non-maxima suppression")
	args = vars(ap.parse_args())

	# load the COCO class labels our YOLO model was trained on
	labelsPath = os.path.sep.join([args["yolo"], "obj.names"])

	# derive the paths to the YOLO weights and model configuration
	weightsPath = os.path.sep.join([args["yolo"], "yolov4-custom-var-out_last.weights"])
	configPath = os.path.sep.join([args["yolo"], "yolov4-custom-var-out.cfg"])
	# load our YOLO object detector trained on COCO dataset (80 classes)
	print("[INFO] loading YOLO from disk...")
	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	#Labels for classes
	LABELS = open(labelsPath).read().strip().split("\n")
	# initialize a list of colors to represent each possible class label
	np.random.seed(42)
	COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

	# load our input image and grab its spatial dimensions
	image = cv2.imread(args["image"])
	(H, W) = image.shape[:2]
	#image = cv2.resize(image, (620, 620))
	#(H, W) = image.shape[:2]

	# determine only the *output* layer names that we need from YOLO
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	# construct a blob from the input image and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes and
	# associated probabilities
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()
	# show timing information on YOLO
	print("[INFO] YOLO took {:.6f} seconds".format(end - start))

	# initialize our lists of detected bounding boxes, confidences, and
	# class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability) of
			# the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to the
				# size of the image, keeping in mind that YOLO actually
				# returns the center (x, y)-coordinates of the bounding
				# box followed by the boxes' width and height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")
				# use the center (x, y)-coordinates to derive the top and
				# and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))
				# update our list of bounding box coordinates, confidences,
				# and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			# draw a bounding box rectangle and label on the image
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			print(text)
			cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,	0.5, color, 2)
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)


def analizeImage(sudoku, net, LABELS, COLORS, confidence, threshold):

	grid_size = [72, 72]
	#sudoku = cv2.resize(sudoku, (450,450))
	(H, W) = sudoku.shape[:2]
	print(sudoku.shape[:2])
	grid = np.zeros(grid_size)
	(H_grid, W_grid) = grid.shape[:2]
	for y in range(int(H/H_grid)):
		for x in range(int(W/W_grid)):
			if(x == 0 and y == 0):
				image = sudoku[y*grid_size[0]:(y+1)*grid_size[0],x*grid_size[1]:(x+1)*grid_size[1]]
			if x== 0 and y != 0:
				image = sudoku[y*grid_size[0]/2:(y+1)*grid_size[0],x*grid_size[1]:(x+1)*grid_size[1]]
			print("x: " + str(x) + " y: " + str(y) + "size: " + str(float(image.sum())))
			if image.sum() > 25000:    
				grid[y][x] = prediction(image, net, LABELS, COLORS, confidence, threshold)
			else:
				grid[y][x] = 0    
	grid =  grid.astype(int)
	print(grid)

def prediction(image, net, LABELS, COLORS, confidence, threshold):
	
	(H, W) = image.shape[:2]
	#image = cv2.resize(image, (620, 620))
	#(H, W) = image.shape[:2]

	# determine only the *output* layer names that we need from YOLO
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	# construct a blob from the input image and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes and
	# associated probabilities
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()
	# show timing information on YOLO
	print("[INFO] YOLO took {:.6f} seconds".format(end - start))

	# initialize our lists of detected bounding boxes, confidences, and
	# class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability) of
			# the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > confidence:
				# scale the bounding box coordinates back relative to the
				# size of the image, keeping in mind that YOLO actually
				# returns the center (x, y)-coordinates of the bounding
				# box followed by the boxes' width and height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")
				# use the center (x, y)-coordinates to derive the top and
				# and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))
				# update our list of bounding box coordinates, confidences,
				# and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			# draw a bounding box rectangle and label on the image
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			print(text)
			return(LABELS[classIDs[i]])

if __name__ == '__main__':

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,	help="path to input image")
	ap.add_argument("-y", "--yolo", required=True,	help="base path to YOLO directory")
	ap.add_argument("-c", "--confidence", type=float, default=0.01,	help="minimum probability to filter weak detections")
	ap.add_argument("-t", "--threshold", type=float, default=0.3,	help="threshold when applying non-maxima suppression")
	args = vars(ap.parse_args())

	# load the COCO class labels our YOLO model was trained on
	labelsPath = os.path.sep.join([args["yolo"], "obj.names"])

	# derive the paths to the YOLO weights and model configuration
	weightsPath = os.path.sep.join([args["yolo"], "yolov4-custom-var-out_last.weights"])
	configPath = os.path.sep.join([args["yolo"], "yolov4-custom-var-out.cfg"])
	# load our YOLO object detector trained on COCO dataset (80 classes)
	print("[INFO] loading YOLO from disk...")
	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	#Labels for classes
	LABELS = open(labelsPath).read().strip().split("\n")
	# initialize a list of colors to represent each possible class label
	np.random.seed(42)
	COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

	image = cv2.imread(args["image"])

	confidence = args["confidence"]
	threshold = args["threshold"]

	analizeImage(image, net, LABELS, COLORS, confidence, threshold)

	#prediction(image, net, LABELS, COLORS)