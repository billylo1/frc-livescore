import numpy as np
import cv2.cv2 as cv

img1 = cv.imread('score_overlay_2021_1280.png', cv.IMREAD_GRAYSCALE)  # queryImage
img2 = cv.imread('2021/frame-00570.jpg', cv.IMREAD_GRAYSCALE)  # trainImage

# Initiate SIFT detector
sift = cv.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]

# Apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
t = cv.estimateAffinePartial2D(src_pts, dst_pts)

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
    cv.polylines(img, [box], True, color, 2, cv.LINE_AA)


box = _cornersToBox(transformPoint((0, 0)), transformPoint((1280, 170)))
_drawBox(img2, box, (255, 255, 0))

img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, [[m] for m in good], None,
                         flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow("Matches", img3)
cv.waitKey()