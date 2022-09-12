import cv2
import time
import poseModule as pm
import PiSeps as ps
import numpy as np
import playsound as pss

def generate_image(img1, img2, ys,xs) :
    h2,w2 = img2.shape[:2]

    for i in range(h2) :
        for j in range(w2) :
            img1[ys + i, xs + j] = img2[i, j] if img2[i, j].all() != 0 else img1[ys + i, xs + j]

    return img1

def check_weight(img, current_duration_for_curl, counter, wrong_position):
    #if (len(self.lm_list) > 16):
    x, y = 950, 310
    if wrong_position :
        cv2.putText(img, f'   Make Your ', (x + 50, y - 100),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f'  Elbow in Line', (x + 50, y - 70),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f'    With Your ', (x + 50, y - 40),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f'    shoulder!', (x + 50, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
    elif current_duration_for_curl > 3 and counter > 6:
        cv2.putText(img, f'Good job just', (x + 80, y - 70), cv2.FONT_HERSHEY_DUPLEX, 1, (76, 153, 0), 2)
        cv2.putText(img, f' remaining {10 - counter}', (x + 80, y - 25),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (76, 153, 0), 2)
    elif current_duration_for_curl > 3 and counter <= 6:
        cv2.putText(img, f'  We are just', (x + 50, y - 100),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f'    in curl {counter}', (x + 50, y - 70),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f'  May be this is', (x + 50, y - 40),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f' a heavy weight', (x + 50, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

def tell_hand_order(img,hand):
    #if (len(self.lm_list) > 16):
    x, y = 950, 320
    cv2.putText(img, f'  {hand} hand ', (x + 70, y - 70),
                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img, f'     Turn ', (x + 70, y - 25),
                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)


def aiTrainer() :
    cap = cv2.VideoCapture(0)
    wcam, hcam = 1000, 1000
    cap.set(3,wcam)
    cap.set(4,hcam)

    pTime = 0
    pose = pm.poseDetector(min_detection_confidence=0.8)
    piStat = ps.PiSeps()
    group = 1
    hand_order = "Right"

    timer = 11
    counter = 0
    hand_cof = 1
    verified_hand = ""

    first_enter = True
    first_time_enter=True
    first_sound_enter=True
    while True :
        success, img = cap.read()
        right_pos, hand = piStat.rightPosture(img)
        cTime = time.time()
        if first_time_enter:
            pTime=cTime
            first_time_enter=False

        if hand == "Right":
            verified_hand = "Right"
        elif hand == "Left":
            verified_hand = "Left"

        if verified_hand == "Left":
            hand_cof= -1
        elif verified_hand == "Right":
            hand_cof= 1

        coach_img = cv2.imread("Images/coach.jpg")
        img = np.concatenate((img, coach_img), axis=1)

        if not timer and hand_order==verified_hand:
            wrong_pos = piStat.wrongElbowPosition(img, verified_hand)
            counter, current_duration_for_curl = piStat.count_curl_and_time(img, hand_cof, verified_hand)
            #print(f'counter in if timer is {counter} and hand_order is {hand_order}')
            check_weight(img, current_duration_for_curl, counter, wrong_pos)
        elif hand_order!=verified_hand :
            tell_hand_order(img, hand_order)
        elif 0<timer<=3:
            cv2.putText(img, f'  BE READY ', (1030, 260),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        if 0<timer<=1:
            if first_sound_enter:
                pss.playsound("E:\\computer_vision_course\\AITrainer\\sounds\\short_whistle.wav")
                first_sound_enter=False


        if cTime - pTime >= 1 and timer > 0:
            timer-=1
            pTime = cTime


        cv2.putText(img, f'Count: ', (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (42, 42, 162), 2)
        cv2.putText(img, f'{counter}', (130, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f'Posture Position: ', (10, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (42, 42, 162), 2)
        cv2.putText(img, f'{right_pos}', (300, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f'Hand: ', (10, 130), cv2.FONT_HERSHEY_DUPLEX, 1, (42, 42, 162), 2)
        cv2.putText(img, f'{verified_hand}', (120, 130), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f'Group: ', (750, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (42, 42, 162), 2)
        cv2.putText(img, f'{group}', (870, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, f'Timer: ', (750, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (42, 42, 162), 2)
        cv2.putText(img, f'{timer}', (870, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

        if counter == 10:
            print(f'in if and counter is {counter}')
            if first_enter:
                group += 1
                #todo change hand every group and set a timer
                hand_order = "Left" if hand_order == "Right" else "Right"
                counter = 0
                timer = 15
                first_enter = False
                first_sound_enter=True

        if counter != 10:
            first_enter = True

        if group == 5 :
            cTime=time.time()
            pTime=cTime
            while cTime-pTime<=1:
                success, img = cap.read()
                coach_img = cv2.imread("Images/coach.jpg")
                img = np.concatenate((img, coach_img), axis=1)
                cv2.putText(img, f' Good Job!! ', (1030, 265),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (76, 153, 0), 2)
                cv2.imshow("AI Trainer", img)
                cv2.waitKey(1)
                cTime=time.time()
            pss.playsound("E:\\computer_vision_course\\AITrainer\\sounds\\long_whistle.wav")
            return True

        cv2.imshow("AI Trainer", img)
        cv2.waitKey(1)

if __name__ == "__main__" :
    aiTrainer()


'''
cTime = time.time()
        if first_enter_to_finish :
            pTime = cTime
            first_enter_to_finish = False
'''
'''
if hand_order!=hand and (timer==0 or timer==-1):
    timer_shown = 0
    timer = -1
elif hand_order==hand and timer==-1:
    timer=0
    timer_shown=timer
else:
    timer_shown=timer

if :
    hand_order_verified=True
else:
    hand_order_verified=False

print(f'hand_order_verified is {hand_order_verified}')
'''
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

# img = coach_img if coach_img.all() != 0 else img
# img = cv2.add(img, coach_img)

# print(wrong_pos)
# print(counter)
# print(timeForCurl)

#        if cTime - pTime >= 5 :
#            group = 4