import cv2
import time
import poseModule as pm
import PiSeps as ps
import numpy as np

def generate_image(img1, img2, ys,xs) :
    h2,w2 = img2.shape[:2]

    for i in range(h2) :
        for j in range(w2) :
            img1[ys + i, xs + j] = img2[i, j] if img2[i, j].all() != 0 else img1[ys + i, xs + j]

    return img1

def check_weight(img, current_duration_for_curl, counter, wrong_position):
    #if (len(self.lm_list) > 16):
    x16, y16 = 950, 320
    if current_duration_for_curl > 2.5 and counter > 6 and not wrong_position:
        cv2.putText(img, f'Good job just', (x16 + 50, y16 - 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, f'remaining {10 - counter}', (x16 + 50, y16 - 25),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    elif current_duration_for_curl > 2.5 and counter <= 6 and not wrong_position:
        cv2.putText(img, f'  We are just', (x16 + 50, y16 - 90),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.putText(img, f'   in curl {counter}', (x16 + 50, y16 - 65),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.putText(img, f' May be this is', (x16 + 50, y16 - 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.putText(img, f'a heavy weight', (x16 + 50, y16 - 15),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

cap = cv2.VideoCapture(0)
wcam, hcam = 1000, 1000
cap.set(3,wcam)
cap.set(4,hcam)

pTime = 0
pose = pm.poseDetector(min_detection_confidence=0.75)
piStat = ps.PiSeps()
group = 0
counter = 0
first_enter = True
while True :
    success, img = cap.read()
    wrong_pos = piStat.wrongPosition(img)
    counter, current_duration_for_curl = piStat.count_curl_and_time(img)
    coach_img = cv2.imread("Images/coach.jpg")
    print(img.shape)
    print(coach_img.shape)

    #img = generate_image(img,coach_img, 120, 630)
    img = np.concatenate((img, coach_img), axis = 1);

    check_weight(img, current_duration_for_curl, counter, wrong_pos)


    #img = coach_img if coach_img.all() != 0 else img

    #img = cv2.add(img, coach_img)

    #print(wrong_pos)
    #print(counter)
    #print(timeForCurl)

    cv2.putText(img, f'count: {counter}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'group: {group}', (700, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    if counter == 10 :
        if first_enter :
            group += 1
            #counter = 0
            first_enter = False

    if counter != 10 :
        first_enter = True

    if group == 4 :
        break

    #cv2.putText(img, f'FPS {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("AI Trainer", img)
    cv2.waitKey(1)


'''
    img = pose.find_pose(img, False)
    lm_list = pose.find_position(img, False)
    if (len(lm_list) > 16):
        angle = pose.find_angle(img, 12,14,16)
        #print(counter)

        if angle <160 and angle > 140 :
            if first_enter :
                pTime = time.time()
                first_enter=False
            got_down = True

        if angle < 60 and got_down:
            #print(time.time())
            #print(pTime)
            timeForCurl = round(time.time()-pTime, 2)
            count_flip = True
            got_down = False

        if count_flip :
            counter +=1
            print(counter)
            print(timeForCurl)
            first_enter = True
            count_flip = False

        if counter == 10:
            counter = 0


        x12,y12 = lm_list[12][1], lm_list[12][2]
        x14, y14 = lm_list[14][1], lm_list[14][2]
        x16, y16 = lm_list[16][1], lm_list[16][2]

        #print(int(x14-x12))
        if int(x14-x12) < -10 :
            wrong_position = True
        else :
            wrong_position=False

        if wrong_position :
            cv2.putText(img, "Wrong Position,Please Fix your elbow", (10,50), cv2.FONT_HERSHEY_PLAIN,2, (0,0,255), 2)
            cv2.putText(img, "Your elbow must be in line with your shoulder", (10, 90), cv2.FONT_HERSHEY_PLAIN,  1, (0, 0, 255),2)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    wrong_position = False
counter =0
count_flip = False
got_down = True
first_enter = True
    '''