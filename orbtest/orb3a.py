import sys
import numpy as np
import cv2.cv2 as cv2

# with the name image.jpg
img1 = cv2.imread('score_overlay_2021_1280.png')
img2 = cv2.imread('2021/frame-00570.jpg')

orb = cv2.ORB_create(nfeatures=1000) # Increasing nfeatures to get more keypoints

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)


matcher = cv2.BFMatcher()
matches = matcher.knnMatch(des1, des2, k=2)

# Apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

print("found {} matches".format(len(good)))

if len(good) < 7:
    print("Not enough good keypoint matches between template and image")
    sys.exit(1)

src_pts = np.float32([kp1[m.queryIdx].pt for m in good])
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])
t = cv2.estimateAffinePartial2D(src_pts, dst_pts)

print("kp1:{} kp2:{}".format(len(src_pts), len(dst_pts)))
