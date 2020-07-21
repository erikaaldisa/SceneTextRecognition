# USAGE
# python3 text_recognition_test.py --east frozen_east_text_detection.pb --image images/example_03.jpg
# python3 text_recognition_test.py --east frozen_east_text_detection.pb --image images/example_04.jpg --padding 0.05
# python3 text_recognition_test.py --east frozen_east_text_detection.pb --image images/img6.jpg

# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	help="path to input image")
ap.add_argument("-east", "--east", type=str,
	help="path to input EAST text detector")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
	help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=320,
	help="nearest multiple of 32 for resized width")
ap.add_argument("-e", "--height", type=int, default=320,
	help="nearest multiple of 32 for resized height")
ap.add_argument("-p", "--padding", type=float, default=0.0,
	help="amount of padding to add to each border of ROI")
args = vars(ap.parse_args())

def decode_predictions(scores, geometry):
	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	print(scores.shape)
	#(1,1,80,80) means 80 rows and cols
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []
	rowscols = []

	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the
		# geometrical data used to derive potential bounding box
		# coordinates that surround text


		scoresData = scores[0, 0, y]
		#print(geometry)
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]
		#print('(xData0,xData1,xData2,xData3,anglesData) - ',(xData0,xData1,xData2,xData3,anglesData))

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability,
			# ignore it
			if scoresData[x] < args["min_confidence"]:
				continue

			# compute the offset factor as our resulting feature
			# maps will be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and
			# then compute the sin and cosine
			# print(y, 'row')
			# print(x, 'column')
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)
			# print(sin,cos)
			rowscols.append((y,x,angle))

			# use the geometry volume to derive the width and height
			# of the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates
			# for the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			# startX = int(endX - w)
			# startY = int(endY - h)
			startX = int(endX +(w*-cos))
			startY = int(endY +(h*-cos))
			#print(startX,startY,endX, endY, point1, point3)

			# add the bounding box coordinates and probability score
			# to our respective lists
			rects.append((startX, startY, endX, endY))
			#print(rects)
			confidences.append(scoresData[x])
		cv2.waitKey(2000)

	# return a tuple of the bounding boxes and associated confidences
	print('length of rowcols that exceeds min confidence of 0.5,',len(rowscols))
	#print(rowscols)
	print('length of rects', len(rects))
	return (rects, confidences)


# load the input image and grab the image dimensions
image = cv2.imread(args["image"])
orig = image.copy()
print('image shape is ',image.shape)
(origH, origW) = image.shape[:2]
#print((origH,origW))
# cv2.imshow("Original Image", orig)
# cv2.waitKey(2000)  #in milliseconds

# set the new width and height and then determine the ratio in change
# for both the width and height
(newW, newH) = (args["width"], args["height"])
print('resized image new width and height - ',(newW,newH))
rW = origW / float(newW)
print('Ratio of W is ',rW)
rH = origH / float(newH)
print('Ratio of H is ',rH)

# resize the image and grab the new image dimensions
image = cv2.resize(image, (newW, newH))
(H, W) = image.shape[:2]
print('resized image shape is ',image.shape)
# cv2.imshow("Resized Image", image)
# cv2.waitKey(2000)  #in milliseconds

# define the two output layer names for the EAST detector model that
# we are interested -- the first is the output probabilities and the
# second can be used to derive the bounding box coordinates of text
layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]

# load the pre-trained EAST text detector
print("[INFO] loading EAST text detector...")
net = cv2.dnn.readNet(args["east"])

# construct a blob from the resized image and then perform a forward pass of
# the model to obtain the two output layer sets
blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
	(123.68, 116.78, 103.94), swapRB=True, crop=False)
start = time.time()
net.setInput(blob)
(scores, geometry) = net.forward(layerNames)
# print('score, geometry - ',(scores,geometry))
end = time.time()

# show timing information on text prediction
print("[INFO] text detection took {:.6f} seconds".format(end - start))

# decode the predictions, then  apply non-maxima suppression to
# suppress weak, overlapping bounding boxes
(rects, confidences) = decode_predictions(scores, geometry)
#print('rects, confidences - ',(rects,confidences))
boxes = non_max_suppression(np.array(rects), probs=confidences)
#print('after Non-Maxima Suppression,\n', boxes)

# initialize the list of results
results = []

# loop over the bounding boxes
for (startX, startY, endX, endY) in boxes:
	# scale the bounding box coordinates based on the respective
	# ratios
	startX = int(startX * rW)
	startY = int(startY * rH)
	endX = int(endX * rW)
	endY = int(endY * rH)

	# in order to obtain a better OCR of the text we can potentially
	# apply a bit of padding surrounding the bounding box -- here we
	# are computing the deltas in both the x and y directions
	dX = int((endX - startX) * args["padding"])
	dY = int((endY - startY) * args["padding"])

	# apply padding to each side of the bounding box, respectively
	startX = max(0, startX - dX)
	startY = max(0, startY - dY)
	endX = min(origW, endX + (dX * 2))
	endY = min(origH, endY + (dY * 2))
	print(startX, startY, endX, endY)

	# extract the actual padded ROI
	#print(orig[startY:endY])
	#print(orig[startX:endX])
	roi = orig[startY:endY, startX:endX]
	#print('roi ', roi)

	# in order to apply Tesseract v4 to OCR text we must supply
	# (1) a language, (2) an OEM flag of 4, indicating that the we
	# wish to use the LSTM neural net model for OCR, and finally
	# (3) an OEM value, in this case, 7 which implies that we are
	# treating the ROI as a single line of text
	config = ("-l eng --oem 1 --psm 7")
	text = pytesseract.image_to_string(roi, config=config)

	# add the bounding box coordinates and OCR'd text to the list
	# of results
	results.append(((startX, startY, endX, endY), text))

# sort the results bounding box coordinates from top to bottom
print('results before sorted, ',results)
results = sorted(results, key=lambda r:r[0][1])
print('results after sorted, ',results)
#[((40, 95, 175, 126), 'ESTATE'), ((187, 100, 338, 129), 'AGENTS'), ((155, 150, 280, 174), 'SAXONS')]
#results_fake= [((40, 95, 175, 126), 'ESTATE'), ((187, 100, 338, 129), 'AGENTS'), ((155, 150, 280, 174), 'SAXONS')]

# Use this if you want to see the text detected one by one
# for ((startX, startY, endX, endY), text) in results:
# 	# display the text OCR'd by Tesseract
# 	print("OCR TEXT")
# 	print("========")
# 	print("{}\n".format(text))

# 	# strip out non-ASCII text so we can draw the text on the image
# 	# using OpenCV, then draw the text and a bounding box surrounding
# 	# the text region of the input image
# 	text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
# 	output = orig.copy()
# 	cv2.rectangle(output, (startX, startY), (endX, endY),
# 		(0, 0, 255), 2)
# 	cv2.putText(output, text, (startX, startY + 80),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# 	# show the output image
# 	cv2.imshow("Text Detection", output)
# 	cv2.waitKey(3000)  #in milliseconds

# Use this if you want to see the text detected all at once
output = orig.copy()
for ((startX, startY, endX, endY), text) in results:
	text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
	cv2.rectangle(output, (startX, startY), (endX, endY),
		(0, 0, 255), 2)
	cv2.putText(output, text, (startX, startY + 80),
		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
# show the output image
cv2.imshow("Text Detection", output)
cv2.waitKey(5000)  #in milliseconds