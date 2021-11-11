import numpy as np
import cv2.cv2 as cv2


# Read the query image as query_img
# and train image This query image
# is what you need to find in train image
# Save it in the same directory
# with the name image.jpg
template = cv2.imread('score_overlay_2021_1280.png')
target = cv2.imread('2021/frame-00570.jpg')

# Convert it to grayscale
# template_bw = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# target_bw = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

# Initialize the ORB detector algorithm
algo = cv2.ORB_create()

# Now detect the keypoints and compute
# the descriptors for the query image
# and train image
template_kp, template_des = algo.detectAndCompute(template, None)
target_kp, target_des = algo.detectAndCompute(target, None)

# Initialize the Matcher for matching
# the keypoints and then match the
# keypoints
matcher = cv2.BFMatcher()
matches = matcher.match(template_des, target_des)
# matches = matcher.knnMatch(template_des, target_des, k=2)

# Apply ratio test
# good = []
# for m,n in matches:
#     if m.distance < 0.75*n.distance:
#         good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
# final_img = cv2.drawMatchesKnn(template,template_kp,target,target_kp,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Show the final image
# cv2.imshow("Matches", final_img)
# cv2.waitKey()

# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)
# matcher = cv2.FlannBasedMatcher(index_params, search_params)
# matches = matcher.knnMatch(template_kp, target_kp, k=2)

# # Apply ratio test
# good = []
# for m,n in matches:
#     if m.distance < 0.75*n.distance:
#         good.append([m])
#
# # cv.drawMatchesKnn expects list of lists as matches.
# final_img = cv2.drawMatchesKnn(template, template_kp,
#                                target, target_kp, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#
# # Show the final image
# cv2.imshow("Matches", final_img)
# cv2.waitKey()

# draw the matches to the final image
# containing both the images the drawMatches()
# function takes both images and keypoints
# and outputs the matched query image with
# its train image
final_img = cv2.drawMatches(template, template_kp,
                            target, target_kp, matches[:20], None)
#
# final_img = cv2.resize(final_img, (1000, 650))
#
# Show the final image
cv2.imshow("Matches", final_img)
cv2.waitKey()