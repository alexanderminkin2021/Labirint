import cv2
from HandTrackingModuleA import HandDetector
import numpy as np

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, maxHands=2)
#--------------
brushThickness = 7
eraserThickness = 100
drawColor = (255, 0, 255)  # setting purple color

xp1, yp1 = 0, 0
xp2,yp2=0,0

x1, y1 = 0, 0
x2,y2=0,0

errX=abs(x2 - xp2)
errY=abs(y2 - yp2)
oldErrX=errX
oldErrY=errY

imgCanvas = np.zeros((800, 1600, 3), np.uint8)  # defining canvas
imgCanvas[:] = (255, 255, 255)#set white color

imgCanvas2 = np.zeros((800, 1600), np.uint8)

cap.set(3, 640)  # width
cap.set(4, 480)  # height

width  =1600# int(cap.get(3))   # float `width`
height =800# int(cap.get(4))  # float `height`

pic = cv2.imread('Folder/spiral.jpg')
pic=cv2.resize(pic,(800,600))

dogPic = cv2.imread('Folder/Forward.png')

dogPicW,dogPicH=dogPic.shape[:2]
print(dogPicH,dogPicW)
# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(dogPic, cv2.COLOR_BGR2HSV)
lower_blue = np.array([0,0,0])
upper_blue = np.array([200,157,255])
mask = cv2.inRange(img2gray,lower_blue, upper_blue)
mask_inv = cv2.bitwise_not(mask)




height2, width2 = pic.shape[:2]
print(height2,width2)
offsetYpic,offsetXpic=300,100
imgCanvas[offsetXpic:offsetXpic+ height2, offsetYpic: offsetYpic+width2] = pic

output=imgCanvas.copy()

switchOn=False
#--------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 2)  # for neglecting mirror inversion

    hands, img = detector.findHands(img, flipType=False)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw
    #print(hands)
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        #print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        # length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw
        x1, y1 = lmList1[8][0], lmList1[8][1]

        y1 = (2*(480 - y1))
        x1 = (2*x1)

        #print('right', x1, y1)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            x2, y2 = lmList2[8][0], lmList2[8][1]
            y2 = (2 * (480 - y2))
            x2 = (2 * x2)
            errX = abs(x2 - xp2)
            errY = abs(y2 - yp2)


            #y2 = 480 - y2
            #print('left',x2,y2)
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            fingers2 = detector.fingersUp(hand2)
           # print(fingers1[2], fingers2[2])
            #length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
            #length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

            if not fingers1[2] and not fingers1[3] and not fingers1[4] or not fingers2[2] and not fingers2[3] and not fingers2[4]:
                switchOn=False
            else:
                switchOn=True
                print('Ok')

            if abs(x1-xp1)>1 and abs(y1-yp1)>1:
                print(abs(x1-xp1))
                #cv2.circle(imgCanvas, (x1, y1), brushThickness, drawColor, cv2.FILLED)  # drawing mode is represented as circle

            # print("Drawing Mode")
            if xp1 == 0 and yp1 == 0:  # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                xp1, yp1 = x1, y1  # so to avoid that we set xp=x1 and yp=y1

            #if abs(x2 - xp2) > 1 and abs(y2 - yp2) > 1:
               # cv2.circle(imgCanvas, (x2, y2), brushThickness, drawColor, cv2.FILLED)  # drawing mode is represented as circle
            # print("Drawing Mode")
            if xp2 == 0 and yp2 == 0:  # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                xp2, yp2 = x2, y2  # so to avoid that we set xp2=x2 and yp2=y2

            if switchOn == False:
                imgCanvas[:] = (255, 255, 255)  # defining canvas
                imgCanvas[offsetXpic:offsetXpic + height2, offsetYpic: offsetYpic + width2] = pic
                   # imgCanvas[int(height / 2 - height2 / 2):int(height / 2 + height2 / 2),
               # int(width / 2 - width2 / 2):int(width / 2 + width2 / 2)] = pic
               # x_offset = x1
               # y_offset = y1
               # imgCanvas[y_offset:y_offset + dogPicW, x_offset:x_offset + dogPicH] = dogPic

            #gonna draw lines from previous coodinates to new positions


            cv2.line(imgCanvas, (xp1, yp1), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp2, yp2), (x2, y2), drawColor, brushThickness)

            x_offset = x1
            y_offset = y1

            '''
            imgCanvas2[y_offset:y_offset + dogPicW, x_offset:x_offset + dogPicH] = mask
            mask_inv = cv2.bitwise_not(imgCanvas2)
            output[y_offset:y_offset + dogPicW, x_offset:x_offset + dogPicH] = dogPic
            img2_fg = cv2.bitwise_and(output, output, mask=imgCanvas2)
            # cv.imshow('res2',img2_fg)

            # Now black-out the area of logo in ROI
            img1_bg = cv2.bitwise_and(imgCanvas, imgCanvas, mask=mask_inv)
            # cv.imshow('res3',img1_bg)

            # Take only region of logo from logo image.
            # img2_fg = cv.bitwise_and(img1,img2,mask = mask)
            # Put logo in ROI and modify the main image
            imgCanvas= cv2.add(img1_bg, img2_fg)

            #imgCanvas2[y_offset:y_offset + dogPicW, x_offset:x_offset + dogPicH] = dogPic
            '''

            xp1, yp1 = x1, y1
            xp2, yp2 = x2, y2


    cv2.imshow("Inv", imgCanvas)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)