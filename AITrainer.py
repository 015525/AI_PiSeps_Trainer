import cv2
import time
import poseModule as pm

cap = cv2.VideoCapture(0)
wcam, hcam = 720, 480
cap.set(3,wcam)
cap.set(4,hcam)

pTime = 0
pose = pm.poseDetector(min_detection_confidence=0.75)
wrong_position = False
counter =0

while True :
    success, img = cap.read()
    img = pose.find_pose(img)
    lm_list = pose.find_position(img)
    if (len(lm_list) > 0):
        x12,y12 = lm_list[12][1], lm_list[12][2]
        x14, y14 = lm_list[14][1], lm_list[14][2]
        x16, y16 = lm_list[16][1], lm_list[16][2]

        print(int(x14-x12))
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

    #cv2.putText(img, f'FPS {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("AI Trainer", img)
    cv2.waitKey(1)