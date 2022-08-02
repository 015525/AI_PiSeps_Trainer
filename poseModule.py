import cv2
import mediapipe as mp
import time

'''
like hand tracking , 
pose tracking have two basis running in the backend
1- pose detection :- crop the pose form image
2- placing land marks :- 33 land marks for whole body 25 for the upper body only
'''

class poseDetector :
    def __init__(self,
                 static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.cmplx = model_complexity
        self.smoothLm = smooth_landmarks
        self.EnableSeg = enable_segmentation
        self.smoothSeg = smooth_segmentation
        self.minDetectConf = min_detection_confidence
        self.minTrackConf= min_tracking_confidence

        self.myPose = mp.solutions.pose
        self.pose = self.myPose.Pose(self.mode,
                                     self.cmplx,
                                     self.smoothLm,
                                     self.EnableSeg,
                                     self.smoothSeg,
                                     self.minDetectConf,
                                     self.minTrackConf)
        self.mpDraw = mp.solutions.drawing_utils



    def find_pose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if draw :
            if self.results.pose_landmarks :
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.myPose.POSE_CONNECTIONS)
        return img

    def find_position(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark) :
                h,w,c=img.shape
                cx,cy = int(lm.x*w) , int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw :
                    cv2.circle(img, (cx,cy), 7, (255,0,0), cv2.FILLED)

        return self.lmList


    def find_angle(self,img, p1, p2, p3, draw = True):
        _,x1,y1 = self.lmList[p1]
        _, x2, y2 = self.lmList[p2]
        _, x3, y3 = self.lmList[p3]

        if draw :
            cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 7, (255, 0, 0), cv2.FILLED)






def main() :
    cap = cv2.VideoCapture('poseVideos/1.mp4')
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()

        img = detector.find_pose(img, draw=False)
        lmList = detector.find_position(img, draw=False)
        if len(lmList) >= 15 :
            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 10, (255,0,0), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == "__main__" :
    main()