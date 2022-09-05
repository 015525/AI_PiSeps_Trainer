import cv2
import time

def generate_image(img1, img2, ys,xs) :
    h2,w2 = img2.shape[:2]

    for i in range(h2) :
        for j in range(w2) :
            img1[ys + i, xs + j] = img2[i, j] if img2[i, j].all() != 0 else img1[ys + i, xs + j]

    return img1

def finish_window() :
    wCam, hCam = 720, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    first_enter = True
    pTime = 0
    while True:
        success, img = cap.read()
        img_1 = cv2.imread("Images/start.png")
        img= generate_image(img, img_1, 5, 240)
        cv2.putText(img, f'See You The Next Exercise', (110, 240), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cTime = time.time()
        if first_enter :
            pTime = cTime
            first_enter = False

        if (cTime-pTime) >= 3:
            break

        cv2.imshow("AI Trainer", img)
        ch = cv2.waitKey(1)

if __name__ == "__main__" :
    finish_window()