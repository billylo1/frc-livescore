import colorsys
import cv2
from PIL import Image
import pkg_resources
from .details import Alliance, OngoingMatchDetails
from .LivescoreBase import LivescoreBase


class Livescore2024(LivescoreBase):
    def __init__(self, **kwargs):
        super(Livescore2024, self).__init__(2024, **kwargs)
        self._match_key = None
        self._match_name = None

    def _getMatchKeyName(self, img, debug_img):
        if self._match_key is None:
            tl = self._transformPoint((320, 6))
            br = self._transformPoint((980, 50))

            raw_match_name = self._parseRawMatchName(self._getImgCropThresh(img, tl, br))
            print('raw_match_name:', raw_match_name)
            # self._match_key = self._getMatchKey(raw_match_name)
            self._match_key = raw_match_name
            if self._match_key:
                self._match_name = raw_match_name
            else:
                self._match_name = raw_match_name

            if self._debug:
                box = self._cornersToBox(tl, br)
                self._drawBox(debug_img, box, (0, 255, 0))

        return self._match_key, self._match_name

    def _getTimeAndMode(self, img, debug_img):
        # Check for match under review
        try :
            horiz_center = img.shape[1]/2

            # review_point1 = self._transformPoint((624, 93))
            # review_sample1 = img[review_point1[1], review_point1[0], :]
            # hsvL = colorsys.rgb_to_hsv(float(review_sample1[2])/255, float(review_sample1[1])/255, float(review_sample1[0])/255)
            # review_point2 = self._transformPoint((1279 - 624, 93))
            # review_sample2 = img[review_point2[1], review_point2[0], :]
            # hsvR = colorsys.rgb_to_hsv(float(review_sample2[2])/255, float(review_sample2[1])/255, float(review_sample2[0])/255)
            # if hsvL[0] > 0.116 and hsvL[0] < 0.216 and hsvR[0] > 0.116 and hsvR[0] < 0.216:
            #     return 0, 'teleop'

            # Find time remaining
            tl = self._transformPoint((horiz_center-60, 125))
            br = self._transformPoint((horiz_center-20, 168))
            time_remaining_minutes = self._parseDigits(self._getImgCropThresh(img, tl, br))
            # print('time_remaining_minutes:', time_remaining_minutes)

            tl2 = self._transformPoint((horiz_center-10, 125))
            br2 = self._transformPoint((horiz_center+60, 168))
            time_remaining_seconds = self._parseDigits(self._getImgCropThresh(img, tl2, br2))
            # print('time_remaining_seconds:', time_remaining_seconds)
            time_remaining = str(time_remaining_minutes) + ":" + str(time_remaining_seconds).zfill(2)
            print('time_remaining:', time_remaining)

            if self._debug:
                # draw a green box for time
                box = self._cornersToBox(tl, br)
                self._drawBox(debug_img, box, (0, 255, 0))
                box2 = self._cornersToBox(tl2, br2)
                self._drawBox(debug_img, box2, (0, 255, 0))

            # Determine mode: 'pre_match', 'auto', 'teleop', or 'post_match'
            mode_point = self._transformPoint((horiz_center-5, 83))
            mode_point2 = self._transformPoint((horiz_center+5, 83))
            mode_sample = img[mode_point[1], mode_point[0], :]
            mode_sample2 = img[mode_point2[1], mode_point2[0], :]

            rgb1 = float(mode_sample[2])/255, float(mode_sample[1])/255, float(mode_sample[0])/255
            rgb2 = float(mode_sample2[2])/255, float(mode_sample2[1])/255, float(mode_sample2[0])/255

            if time_remaining is None:
                return None, None

            if rgb1[0] > 0.5 and rgb2[0] > 0.5 and time_remaining_seconds <= 15 and time_remaining_minutes == 0:
                mode = 'auto'
            else:
                mode = 'teleop'

            if self._debug:
                box = self._cornersToBox(tl, br)
                self._drawBox(debug_img, box, (0, 255, 0))
                # cv2.circle(debug_img, review_point1, 2, (0, 255, 0), -1)
                # cv2.circle(debug_img, review_point2, 2, (0, 255, 0), -1)
                cv2.circle(debug_img, mode_point, 2, (0, 255, 0), -1)
                cv2.circle(debug_img, mode_point2, 2, (0, 255, 0), -1)
                # print('rgb1:', rgb1, 'rgb2:', rgb2)

            return time_remaining, mode
        except:
            return 0, 'teleop'

    def _getFlipped(self, img, debug_img):
        # Sample point to determine red/blue side
        color_point = self._transformPoint((520, 95))
        color_sample = img[color_point[1], color_point[0], :]
        is_flipped = color_sample[0] > color_sample[2]  # More blue than red

        if self._debug:
            cv2.circle(debug_img, color_point, 2, (0, 255, 0), -1)

        return is_flipped

    def _getScores(self, img, debug_img, is_flipped):

        horiz_center = img.shape[1]/2

        # Left score limits
        left_tl = self._transformPoint((horiz_center-270, 70))
        left_br = self._transformPoint((horiz_center-80, 165))
        # Right score limits
        right_tl = self._transformPoint((horiz_center+80, 70))
        right_br = self._transformPoint((horiz_center+270, 165))

        left_score = self._parseDigits(self._getImgCropThresh(img, left_tl, left_br, white=True))
        right_score = self._parseDigits(self._getImgCropThresh(img, right_tl, right_br, white=True))
        print(left_score, right_score)

        if is_flipped:
            red_score = right_score
            blue_score = left_score
        else:
            red_score = left_score
            blue_score = right_score

        if self._debug:
            left_box = self._cornersToBox(left_tl, left_br)
            right_box = self._cornersToBox(right_tl, right_br)
            self._drawBox(debug_img, left_box, (255, 255, 0) if is_flipped else (255, 0, 255))
            self._drawBox(debug_img, right_box, (255, 0, 255) if is_flipped else (255, 255, 0))

        return red_score, blue_score

    def _getTeams(self, img, debug_img, is_flipped):

        horiz_center = img.shape[1]/2
        width = img.shape[1]

        # left_tl1 = self._transformPoint((10, 60))
        # left_br1 = self._transformPoint((horiz_center-230, 95))
        # raw_left_team_numbers = self._parseRawMatchName(self._getImgCropThresh(img, left_tl1, left_br1))
        # print(raw_left_team_numbers)
        
        # Left score limits
        left_tl1 = self._transformPoint((10, 123))
        left_br1 = self._transformPoint((130, 162))

        left_tl2 = self._transformPoint((131, 123))
        left_br2 = self._transformPoint((255, 162))

        left_tl3 = self._transformPoint((256, 123))
        left_br3 = self._transformPoint((355, 162))

        # Right score limits

        right_tl1 = self._transformPoint((width-365, 123))
        right_br1 = self._transformPoint((width-250, 162))

        right_tl2 = self._transformPoint((width-249, 123))
        right_br2 = self._transformPoint((width-127, 162))

        right_tl3 = self._transformPoint((width-126, 123))
        right_br3 = self._transformPoint((width-20, 162))


        left_team1 = self._parseDigits(self._getImgCropThresh(img, left_tl1, left_br1, white=False))
        left_team2 = self._parseDigits(self._getImgCropThresh(img, left_tl2, left_br2, white=False))
        left_team3 = self._parseDigits(self._getImgCropThresh(img, left_tl3, left_br3, white=False))

        right_team1 = self._parseDigits(self._getImgCropThresh(img, right_tl1, right_br1, white=False))
        right_team2 = self._parseDigits(self._getImgCropThresh(img, right_tl2, right_br2, white=False))
        right_team3 = self._parseDigits(self._getImgCropThresh(img, right_tl3, right_br3, white=False))

        left_teams = [left_team1, left_team2, left_team3]
        right_teams = [right_team1, right_team2, right_team3]

        if is_flipped:
            red_teams = right_teams
            blue_teams = left_teams
        else:
            red_teams = left_teams
            blue_teams = right_teams

        if self._debug:
            left_box1 = self._cornersToBox(left_tl1, left_br1)
            left_box2 = self._cornersToBox(left_tl2, left_br2)
            left_box3 = self._cornersToBox(left_tl3, left_br3)

            right_box1 = self._cornersToBox(right_tl1, right_br1)
            right_box2 = self._cornersToBox(right_tl2, right_br2)
            right_box3 = self._cornersToBox(right_tl3, right_br3)

            self._drawBox(debug_img, left_box1, (0, 255, 0) if not is_flipped else (255, 0, 255))
            self._drawBox(debug_img, left_box2, (0, 255, 0) if not is_flipped else (255, 0, 255))
            self._drawBox(debug_img, left_box3, (0, 255, 0) if not is_flipped else (255, 0, 255))
            self._drawBox(debug_img, right_box1, (0, 0, 255) if not is_flipped else (255, 255, 0))
            self._drawBox(debug_img, right_box2, (0, 0, 255) if not is_flipped else (255, 255, 0))
            self._drawBox(debug_img, right_box3, (0, 0, 255) if not is_flipped else (255, 255, 0))

        # red_teams = 1,2,3
        # blue_teams = 4,5,6

        return red_teams, blue_teams


    def _getMatchDetails(self, img, force_find_overlay):

        try:
            debug_img = None
            if self._debug:
                debug_img = img.copy()

            time_remaining, mode = self._getTimeAndMode(img, debug_img)
            if self._is_new_overlay or force_find_overlay:
                self._match_key = None
            match_key, match_name = self._getMatchKeyName(img, debug_img)
            # is_flipped = self._getFlipped(img, debug_img)
            red_score, blue_score = self._getScores(img, debug_img, False)
            red_teams, blue_teams = self._getTeams(img, debug_img, False)

            box = self._cornersToBox(self._transformPoint((0,0)), self._transformPoint((1280, 170)))
            self._drawBox(debug_img, box, (255, 255, 0))

            if self._debug:
                cv2.imshow("ROIs", debug_img)
                cv2.waitKey(10000000)

            # if match_key is not None:        
            if match_key is not None and red_score is not None  \
                    and blue_score is not None and time_remaining is not None:
                return OngoingMatchDetails(
                    match_key=match_key,
                    match_name=match_name,
                    mode=mode,
                    time=time_remaining,
                    red=Alliance(
                        score=red_score,
                        teams=red_teams
                    ),
                    blue=Alliance(
                        score=blue_score,
                        teams=blue_teams
                    )
                )
            else:
                return None
        except Exception as e:
            print(e)
            return None