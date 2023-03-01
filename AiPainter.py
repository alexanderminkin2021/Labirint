import cv2
import time
import HandTrackingModule as htm
import numpy as np
import os

def example():
    overlayList = []  # list to store all the images

    brushThickness = 2
    eraserThickness = 100
    drawColor = (255, 0, 255)  # setting purple color

    xp, yp = 0, 0
    #imgCanvas = np.zeros((480, 640, 3), np.uint8)  # defining canvas
    imgCanvas = np.zeros((480, 640, 3), np.uint8)
    imgCanvas[:] = (255, 255, 255)
    # images in header folder
    folderPath = "Folder"
    myList = os.listdir(folderPath)  # getting all the images used in code
    # print(myList)
    for imPath in myList:  # reading all the images from the folder
        image = cv2.imread(f'{folderPath}/{imPath}')
        image=cv2.resize(image,(640,50))
        overlayList.append(image)  # inserting images one by one in the overlayList
    header = overlayList[0]  # storing 1st image
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)  # width
    cap.set(4, 480)  # height

    width  = int(cap.get(3))   # float `width`
    height = int(cap.get(4))  # float `height`


    pic = cv2.imread('Folder/labirint.jpg')
    height2, width2 = pic.shape[:2]

    imgCanvas[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),
    int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)] = pic

    detector = htm.handDetector(detectionCon=0.50, maxHands=2)  # making object

    switchOn=False

    while True:

        # 1. Import image
        success, img = cap.read()
        img = cv2.flip(img, 2)  # for neglecting mirror inversion

        # 2. Find Hand Landmarks
        img = detector.findHands(img)  # using functions for connecting landmarks
        lmList, bbox, hands_status = detector.findPosition(img,draw=True)  # using function to find specific landmark position,draw false means no circles on landmarks

        if  hands_status['Left']==True:
            print("Left HAND")
            lmList, bbox, hands_status = detector.findPosition(img,draw=False)  # using function to find specific landmark position,draw false means no circles on landmarks
            print(lmList)
            fingers = detector.fingerUp()
            #print(fingers)

        if hands_status['Right'] == True:
            print("Right HAND")
            lmList, bbox, hands_status = detector.findPosition(img,draw=False)  # using function to find specific landmark position,draw false means no circles on landmarks
            print(lmList)
            fingers = detector.fingerUp()
            # print(fingers)

        if len(lmList) != 0:
            # print(lmList)
            x1, y1 = lmList[8][1], lmList[8][2]  # tip of index finger
            x2, y2 = lmList[12][1], lmList[12][2]  # tip of middle finger
            x1=x1
            y1=y1
            y1=480-y1
            # 3. Check which fingers are up
            fingers = detector.fingerUp()
            #print(fingers)

            # 4. If Selection Mode - Two finger are up
            ''' if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                # print("Selection Mode")
                # checking for click
                if y1 < 25:
                    if 25 < x1 < 45:  # if i m clicking at purple brush
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                    elif 55 < x1 < 75:  # if i m clicking at blue brush
                        header = overlayList[1]
                        drawColor = (255, 0, 0)
                    elif 80 < x1 < 95:  # if i m clicking at green brush
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 105 < x1 < 120:  # if i m clicking at eraser
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor,
                              cv2.FILLED)  # selection mode is represented as rectangle
                '''

            if fingers[0] == False and fingers[1] == False and (hands_status['Right_index'] == 1 or (hands_status['Right_index'] == 0 and hands_status['Left'] == False)):
                switchOn=True
            if fingers[0] == False and fingers[1] == False and fingers[2] == False and fingers[3] == False and fingers[4] == False:
                switchOn=False

            # 5. If Drawing Mode - Index finger is up
            if fingers[1] == False and (hands_status['Right_index']==1 or (hands_status['Right_index']==0 and hands_status['Left']==False)):
                #length, img, lineInfo = detector.findDistance(8, 12, img, draw=True)
                #if length < 20:
                cv2.circle(imgCanvas, (x1, y1), 2, drawColor, cv2.FILLED)  # drawing mode is represented as circle
                # print("Drawing Mode")
                if xp == 0 and yp == 0:  # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                    xp, yp = x1, y1  # so to avoid that we set xp=x1 and yp=y1
                # till now we are creating our drawing but it gets removed as everytime our frames are updating so we have to define our canvas where we can draw and show also

                # eraser
                '''if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                '''

                   # imgCanvas = np.zeros((480, 640, 3), np.uint8)
                if switchOn==False:
                    imgCanvas[:] = (255, 255, 255)# defining canvas
                    imgCanvas[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)] = pic

                #cv2.line(img, (xp, yp), (x1, y1), drawColor,brushThickness)  # gonna draw lines from previous coodinates to new positions
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)


                xp, yp = x1, y1  # giving values to xp,yp everytime

            # merging two windows into one imgcanvas and img

        # 1 converting img to gray
       # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

        # 2 converting into binary image and then inverting
       # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

        #imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)  # converting again to gray bcoz we have to add in a RGB image i.e img

        # add original img with imgInv ,by doing this we get our drawing only in black color
        #img = cv2.bitwise_and(img, imgInv)

        # add img and imgcanvas,by doing this we get colors on img
        #img = cv2.bitwise_or(img, imgCanvas)

        # setting the header image
       # img[0:50, 0:640] = header  # on our frame we are setting our JPG image acc to H,W of jpg images

            if x1>width/2 and x1<width and y1<120 and switchOn==True:# if you get finish maze
                break

        cv2.imshow("Image", img)
        #cv2.imshow("Canvas", imgCanvas)

        cv2.imshow("Inv", imgCanvas)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    print("Ok")

    cv2.imwrite('Folder/labirint4.jpg', imgCanvas)
    cap.release()
    cv2.destroyAllWindows()



    #check labirint

    imgNew = cv2.imread('Folder/labirint4.jpg')
    pic=imgNew
    height2, width2 = pic.shape[:2]
    print(width2)
    print(height2)
    width2 = 373
    height2 = 458
    pic = pic[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),
          int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)]

    imgCanvas = np.zeros((480, 640, 3), np.uint8)  # defining canvas
    imgCanvas[:] = (255, 255, 255)
    imgCanvas[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),
    int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)] = pic

    imgMask = np.zeros((480, 640, 3), np.uint8)  # defining canvas
    mask = cv2.imread('Folder/labirintMask.jpg')
    imgMask[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),
    int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)] = mask

    imgGray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

    # 2 converting into binary image and then inverting
    _, imgInv = cv2.threshold(imgGray, 150, 255,
                              cv2.THRESH_BINARY_INV)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

    imgMask = cv2.cvtColor(imgInv,
                           cv2.COLOR_GRAY2BGR)  # converting again to gray bcoz we have to add in a RGB image i.e img

    # add original img with imgInv ,by doing this we get our drawing only in black color
    img = cv2.bitwise_and(imgCanvas, imgMask)

    _, thresh = cv2.threshold(img, 190, 255,
                              cv2.THRESH_BINARY)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

    hsv = cv2.cvtColor(thresh, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (140, 200, 200), (150, 255, 255))
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    edged = cv2.Canny(mask, 30, 255)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # фильтр по площади
    s1 = 0
    for cnt in cnts:
        s1 += cv2.contourArea(cnt)

    # вывод на печать
    print("\nDots number: {}".format(s1))
    fontFace = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 0.7
    thickness = 2
    text_color = (255, 0, 0)
    text_color_bg = (200, 200, 200)

    if switchOn == True and s1 == 0:
       text = "Лабиринт пройден, нажмите ESC"
    else:
       text = "Лабиринт не пройден, нажмите ESC"

    x, y = int(width2 / 2)-50, int(height2 / 2)
    text_size, _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
    text_w, text_h = text_size
    pos = (x, y)
    cv2.rectangle(imgNew, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(imgNew, text, (x, y + text_h), fontFace, fontScale, text_color, thickness)

    cv2.imshow("Result", imgNew)
    while True:

        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


