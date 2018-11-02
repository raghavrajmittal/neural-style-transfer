# USAGE
# python neural_style_transfer_video.py --models models

# import the necessary packages
from imutils.video import VideoStream
from imutils import paths
import itertools
import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--models", required=True,
	help="path to directory containing neural style transfer models")
args = vars(ap.parse_args())

# grab the paths to all neural style transfer models in our 'models'
# directory, provided all models end with the '.t7' file extension
modelPaths = paths.list_files(args["models"], validExts=(".t7",))
modelPaths = sorted(list(modelPaths))

# generate unique IDs for each of the model paths, then combine the
# two lists together
models = list(zip(range(0, len(modelPaths)), (modelPaths)))

# use the cycle function of itertools that can loop over all model
# paths, and then when the end is reached, restart again
# modelIter = itertools.cycle(models)
# (modelID, modelPath) = next(modelIter)
idx = 0
(modelID, modelPath) = models[idx % len(models)]

# load the neural style transfer model from disk
print("[INFO] loading style transfer model...")
net = cv2.dnn.readNetFromTorch(modelPath)

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
print("[INFO] {}. {}".format(modelID + 1, modelPath))

originalCount, styledCount = 0,0
# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()

	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image dimensions
	frame = imutils.resize(frame, width=600)
	orig = frame.copy()
	(h, w) = frame.shape[:2]

	# construct a blob from the frame, set the input, and then perform a
	# forward pass of the network
	blob = cv2.dnn.blobFromImage(frame, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)
	output = net.forward()

	# reshape the output tensor, add back in the mean subtraction, and
	# then swap the channel ordering
	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	output /= 255.0
	output = output.transpose(1, 2, 0)

	# show the original frame along with the output neural style transfer
	cv2.imshow("Input", frame)
	cv2.imshow("Output", output)

	key = cv2.waitKey(1) & 0xFF

	# if the `n` key is pressed (for "next"), load the next neural style transfer model
	if key == ord("n"):
		# (modelID, modelPath) = next(modelIter)
		idx += 1
		(modelID, modelPath) = models[idx % len(models)]
		cv2.putText(frame, str(modelPath.split('/')[-1].split(".")[0]) ,(10,40), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255) , 2)
		cv2.imshow("Input", frame)
		cv2.waitKey(20)
		print("[INFO] {}. {}".format(modelID + 1, modelPath))
		net = cv2.dnn.readNetFromTorch(modelPath)

	# if the `p` key is pressed (for "previous"), load the previous neural style transfer model
	elif key == ord("p"):
		idx -= 1
		(modelID, modelPath) = models[idx % len(models)]
		cv2.putText(frame, str(modelPath.split('/')[-1].split(".")[0]) ,(10,40), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255) , 2)
		cv2.imshow("Input", frame)
		cv2.waitKey(20)
		print("[INFO] {}. {}".format(modelID + 1, modelPath))
		net = cv2.dnn.readNetFromTorch(modelPath)
	# save the actual image
	elif key == ord("a"):
		originalCount += 1
		cv2.imwrite( 'screenshots/original_' + str(originalCount) + ".png", frame)

	#save the styled image
	elif key == ord("s"):
		styledCount += 1
		output *= 255.0
		cv2.imwrite('screenshots/styled_' + str(styledCount) + "_" + str(modelPath.split('/')[-1].split(".")[0]) + ".png", output)

	#save both the images
	elif key == ord("b"):
		styledCount = max(styledCount + 1, originalCount + 1)
		originalCount = styledCount
		output *= 255.0
		cv2.imwrite('screenshots/original_' + str(originalCount) + "_" + str(modelPath.split('/')[-1].split(".")[0]) + ".png", frame)
		cv2.imwrite('screenshots/styled_' + str(styledCount) + "_" + str(modelPath.split('/')[-1].split(".")[0]) + ".png", output)

	# otheriwse, if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
