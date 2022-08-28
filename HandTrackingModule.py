import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 model_complexity=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.numHands = max_num_hands
        self.modelcomplx = model_complexity
        self.minDetectionConf = min_detection_confidence
        self.minTrackingConf = min_tracking_confidence

        self.myhands = mp.solutions.hands
        self.hands = self.myhands.Hands(self.mode, self.numHands,self.modelcomplx, self.minDetectionConf, self.minTrackingConf)
        self.mpdraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw :
                    self.mpdraw.draw_landmarks(img, handlms, self.myhands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)  # 25 is the radius

        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    ctime = 0
    ptime = 0
    handDetector = HandDetector()
    while True:
        success, img = cap.read()
        img = handDetector.findHands(img)
        lmlist = handDetector.find_position(img)
        if len(lmlist) != 0 :
            print(lmlist[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)  # first 3 is scale, second is thickness

        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()