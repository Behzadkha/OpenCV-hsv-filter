import cv2
import numpy as np

cap = cv2.VideoCapture(0) #webcam

def doNothing(x):
	pass
# Control page
cv2.namedWindow("Control") 
cv2.createTrackbar("LowerHue", "Control", 0, 255, doNothing)
cv2.createTrackbar("LowerSaturation", "Control", 0, 255, doNothing)
cv2.createTrackbar("LowerValue", "Control", 0, 255, doNothing)
cv2.createTrackbar("UpperHue", "Control", 255, 255, doNothing)
cv2.createTrackbar("UpperSaturation", "Control", 255, 255, doNothing)
cv2.createTrackbar("UpperValue", "Control", 255, 255, doNothing)
cv2.resizeWindow("Control", 900,50)



while True:
	ret, frame = cap.read()
	## COLOR DETECTION ##
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower_hue = cv2.getTrackbarPos("LowerHue", "Control")
	lower_sat = cv2.getTrackbarPos("LowerSaturation", "Control")
	lower_value = cv2.getTrackbarPos("LowerValue", "Control")
	upper_hue = cv2.getTrackbarPos("UpperHue", "Control")
	upper_sat = cv2.getTrackbarPos("UpperSaturation", "Control")
	upper_value = cv2.getTrackbarPos("UpperValue", "Control")


	lower_blue = np.array([lower_hue, lower_sat, lower_value])
	upper_blue = np.array([upper_hue, upper_sat, upper_value])

	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	res = cv2.bitwise_and(frame, frame, mask=mask)

	median = cv2.medianBlur(res, 5)#less noise
	kernel = np.ones((5,5), np.uint8)
	opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)


	edges = cv2.Canny(frame, 100, 200)
	cv2.imshow('edges', edges)#show edges

	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', opening)
	if cv2.waitKey(20) & 0xFF == ord('q'): # close everyting if q is pressed
		break
cap.release()
cv2.destroyAllWindows()