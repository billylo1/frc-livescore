import numpy as np
import cv2.cv2 as cv2

img1 = cv2.imread('score_overlay_2021_1280.png')  # queryImage
img2 = cv2.imread('2021/frame-00570.jpg')  # trainImage

# Initiate SIFT detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# create BFMatcher object
bf = cv2.BFMatcher() #cv2.NORM_HAMMING, crossCheck=True

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
# matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, flags=2)

cv2.imshow("Matches", img3)
cv2.waitKey()
