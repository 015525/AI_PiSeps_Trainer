import poseModule as pm
import cv2
import time


class PiSeps :
    def __init__(self):
        self.count =0
        self.pose = pm.poseDetector();
        self.wrong_position = False
        self.counter = 0
        self.count_flip = False
        self.got_down = True
        self.first_enter = True
        self.timeForCurl = -1
        self.pTime = time.time()

    def wrongPosition(self, img):
        img = self.pose.find_pose(img, False)
        self.lm_list = self.pose.find_position(img, False)
        if (len(self.lm_list) > 16):
            x12, y12 = self.lm_list[12][1], self.lm_list[12][2]
            x14, y14 = self.lm_list[14][1], self.lm_list[14][2]

            #print(int(x14-x12))
            if int(x14 - x12) < -15:
                self.wrong_position = True
            else:
                self.wrong_position = False

            if self.wrong_position:
                cv2.putText(img, "X", (x14-50, y14+30), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 6)

        return self.wrong_position;

    def count_curl_and_time(self, img):
        angle = self.pose.find_angle(img, 12, 14, 16, draw=False)
        #print(angle)

        if angle < 160 and angle > 140 and not self.wrong_position:
            if self.first_enter:
                self.pTime = time.time()
                self.first_enter = False
            self.got_down = True

        if angle < 60 and self.got_down and angle != -1 and not self.wrong_position:
            # print(time.time())
            # print(pTime)
            self.timeForCurl = round(time.time() - self.pTime, 2)
            self.count_flip = True
            self.got_down = False

        if self.count_flip:
            self.counter += 1
            #print(self.counter)
            #print(self.timeForCurl)
            self.first_enter = True
            self.count_flip = False

        if self.counter > 10:
            self.counter = 1

        #self.check_weight(img, time.time()-self.pTime)

        return self.counter, time.time()-self.pTime
'''

    def check_weight(self, img, current_duration_for_curl):
        if (len(self.lm_list) > 16):
            x16, y16 = 950, 320
            if current_duration_for_curl > 2.5 and self.counter > 6 and not self.wrong_position:
                cv2.putText(img, f'Good job just', (x16+50, y16-70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(img, f'remaining {10 - self.counter}', (x16 + 50, y16 - 25),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif current_duration_for_curl > 2.5 and self.counter <= 6 and not self.wrong_position:
                cv2.putText(img, f'  We are just', (x16+50, y16-90),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.putText(img, f'   in curl {self.counter}', (x16 + 50, y16 - 65),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.putText(img, f' May be this is', (x16+50, y16-40),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.putText(img, f'a heavy weight', (x16 + 50, y16 -15),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
'''