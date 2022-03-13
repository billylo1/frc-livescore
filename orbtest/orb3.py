import sys

import numpy as np
import cv2.cv2 as cv2


# Read the query image as query_img
# and train image This query image
# is what you need to find in train image
# Save it in the same directory
# with the name image.jpg
img1 = cv2.imread('score_overlay_2021_1280.png')
img2 = cv2.imread('2021/frame-00570.jpg')
# img2 = cv2.imread('2021/rr-none.png')

# Initialize the ORB detector algorithm
orb = cv2.ORB_create(nfeatures=1000) # Increasing nfeatures to get more keypoints

# Now detect the keypoints and compute
# the descriptors for the query image
# and train image
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Initialize the Matcher for matching
# the keypoints and then match the
# keypoints
matcher = cv2.BFMatcher()
# matches = matcher.match(des1, des2)
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

src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
t = cv2.estimateAffinePartial2D(src_pts, dst_pts)

print(t)

transform = {
    'scale': t[0][0, 0],
    'tx': t[0][0, 2],
    'ty': t[0][1, 2],
}
TEMPLATE_SCALE = 1


def transformPoint(point):
    # Transforms a point from template coordinates to image coordinates
    scale = transform['scale'] * TEMPLATE_SCALE
    tx = transform['tx']
    ty = transform['ty']
    return np.int32(np.round(point[0] * scale + tx)), np.int32(np.round(point[1] * scale + ty))


def _cornersToBox(tl, br):
    return np.array([
        [tl[0], tl[1]],
        [br[0], tl[1]],
        [br[0], br[1]],
        [tl[0], br[1]]
    ])


def _drawBox(img, box, color):
    cv2.polylines(img, [box], True, color, 2, cv2.LINE_AA)


box = _cornersToBox(transformPoint((0, 0)), transformPoint((1280, 170)))
_drawBox(img2, box, (255, 255, 0))


scale_factor = .75
img3 = cv2.resize(img2, (
    np.int32(np.round(img2.shape[1] * scale_factor)),
    np.int32(np.round(img2.shape[0] * scale_factor))
))

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [[m] for m in good], None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("Matches", img3)
cv2.waitKey()
