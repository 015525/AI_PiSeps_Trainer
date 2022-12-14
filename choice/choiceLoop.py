import cv2
from choice import Choice as cho
import time


def generate_image(img1, img2, ys,xs) :
    h2,w2 = img2.shape[:2]

    for i in range(h2) :
        for j in range(w2) :
            img1[ys + i, xs + j] = img2[i, j] if img2[i, j].all() != 0 else img1[ys + i, xs + j]

    return img1

def choice() :
    wCam, hCam = 720, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    choice = cho.Choice()

    first_enter_1 = True
    pTime = 0
    while True:
        success, img = cap.read()
        img_1 = cv2.imread("Images/start.png")
        img_2 = cv2.imread("Images/thumb_up.png")

        img= generate_image(img, img_1, 5, 240)
        img = generate_image(img, img_2, 167, 426)
        cv2.putText(img, f'If ready then ', (200, 210), cv2.FONT_HERSHEY_DUPLEX, 1,
                    (0, 0, 0), 2)
        cv2.rectangle(img, (200, 220), (460, 460), (42, 42, 162), 3)

        cTime = time.time()
        is_thumb_up, xb1, xb2, yb1 = choice.get_choice(img)

        if is_thumb_up and xb1<470 and  xb2>180 and yb1>180:# and yb2<470 :
            #print("in first if")
            if first_enter_1 :
                pTime = cTime
                first_enter_1 = False
            if (cTime-pTime) >= 2 :
                #print("start exercise")
                return "start exercise"
        else :
            first_enter_1 = True

        cv2.imshow("AI Trainer", img)
        ch = cv2.waitKey(1)

if __name__ == "__main__" :
    choice()


#h1, w1, c1 = img_1.shape
#h2, w2, c2 = img_2.shape

# img[5:5 + h1, 220: 220 + w1] = img_1
# img[330:330 + h2, 330: 330 + w2] = img_2

# print(is_thumb_up, xb1, xb2, yb1)