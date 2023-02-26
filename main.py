import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)
width  = int(cap.get(3))   # float `width`
height = int(cap.get(4))  # float `height`
print(width)
print(height)

pic = cv2.imread('Folder/labirint4.jpg')

height2, width2 = pic.shape[:2]
print(width2)
print(height2)
width2=373
height2=458
pic=pic[int(height/2-height2/2):int(height/2+height2/2), int(width/2-width2/2):int(width/2+width2/2)]

imgCanvas = np.zeros((480, 640, 3), np.uint8)  # defining canvas
imgCanvas[:]=(255,255,255)
imgCanvas[int(height/2-height2/2):int(height/2+height2/2), int(width/2-width2/2):int(width/2+width2/2)] = pic


imgMask = np.zeros((480, 640, 3), np.uint8)  # defining canvas
mask = cv2.imread('Folder/labirintMask.jpg')
imgMask[int(height/2-height2/2):int(height/2+height2/2), int(width/2-width2/2):int(width/2+width2/2)] = mask



imgGray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

# 2 converting into binary image and then inverting
_, imgInv = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

imgMask = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)  # converting again to gray bcoz we have to add in a RGB image i.e img

# add original img with imgInv ,by doing this we get our drawing only in black color
img = cv2.bitwise_and(imgCanvas, imgMask)

_, thresh = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask


hsv = cv2.cvtColor(thresh, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,(140, 200, 200), (150, 255, 255) )
kernel = np.ones((2,2),np.uint8)
mask = cv2.erode(mask,kernel,iterations = 1)
cv2.imshow("orange", mask);


edged = cv2.Canny(mask, 30, 255)
#cv2.imshow('edged',edged)
# findcontours
cnts, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#cnts,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# фильтр по площади
s1 = 0
xcnts = []
for cnt in cnts:
    s1+=cv2.contourArea(cnt)

# вывод на печать
print("\nDots number: {}".format(s1))

fontFace = cv2.FONT_HERSHEY_COMPLEX
fontScale = 0.7
thickness = 2
text_color = (255, 0, 0)
text_color_bg = (200, 200, 200)

if s1 == 0:
    text = "Лабиринт пройден, нажмите ESC"
else:
    text = "Лабиринт не пройден, нажмите ESC"

x, y = int(width2 / 2), int(height2 / 2)
text_size, _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
text_w, text_h = text_size
pos = (x, y)
cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
cv2.putText(img, text, (x, y + text_h ), fontFace, fontScale, text_color, thickness)

# add img and imgcanvas,by doing this we get colors on img
#img = cv2.bitwise_or(img, imgCanvas)


while True:
    cv2.imshow('pic',img)
    #cv2.imshow('mask',imgMask)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
"""
cap = cv2.VideoCapture(2)

while True:
    succes, img=cap.read()

    cv2.imshow("image",img)
    cv2.waitKey(1)
"""