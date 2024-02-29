import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirt_path = ""

with open("shirt_path.txt", "r") as file:
    shirt_path = file.read().strip()

shirt_img = cv2.imread(shirt_path,cv2.IMREAD_UNCHANGED)

fixedRatio = 262/190
shirtRatioWidthHeight = 581/440
imageNumber = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    #img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    #print(lmList)
    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        #imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        try:
            shirt_img = cv2.resize(shirt_img, (widthOfShirt, int(widthOfShirt * shirtRatioWidthHeight)))
        except:
            pass

        currentScale = (lm11[0] - lm12[0])/190
        offSet = int(44 * currentScale),int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img,shirt_img,(lm12[0]-offSet[0],lm12[1]-offSet[1]))
            # img = cvzone.overlayPNG(img,imgButton,(248,150))
        except:
            pass

    cv2.imshow("Virtual Shirt Try-On", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty('Virtual Shirt Try-On', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

#C:/Users/ragha/PycharmProjects/BE/Resources/Glasses/5.png