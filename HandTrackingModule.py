import time
import cv2 as cv
import mediapipe as mp
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2,complexity=1, detectionCon=0.5, trackCon=0.5):  # default initializations
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.tackCon = trackCon
        # initializations
        self.comlexity = complexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.comlexity, self.detectionCon, self.tackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, image, draw=True):
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return image

    def findPosition(self,image, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        self.hands_status = {'Right': False, 'Left': False, 'Right_index': None, 'Left_index': None}
        #getHandType
        if self.results.multi_handedness:


            for hand_index, hand_info in enumerate(self.results.multi_handedness):
                # Retrieve the label of the found hand.
                hand_type = hand_info.classification[0].label
                # Update the status of the found hand.
                self.hands_status[hand_type] = True

                # Update the index of the found hand.
                self.hands_status[hand_type + '_index'] = hand_index

                # Write the hand type on the output image.
            # cv.putText(image, hand_type + ' Hand Detected', (10, (hand_index + 1) * 30), cv.FONT_HERSHEY_PLAIN,2, (0, 255, 0), 2)

        if self.results.multi_hand_landmarks:
            for hand_index, handLandmarks in enumerate(self.results.multi_hand_landmarks):
                xList = []
                yList = []
                bbox = []
                self.lmList = []
                for idNumber, landmarkInformation in enumerate(handLandmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(landmarkInformation.x * w), int(landmarkInformation.y * h)
                    # print(idNumber, cx, cy)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([idNumber,cx,cy])

                    # if idNumber == 4:
                    '''if draw:
                        if idNumber == 0:
                            cv.circle(image, (cx, cy), 25, (5, 5, 5), cv.FILLED)
                        else:
                            cv.circle(image, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    '''
                    xmin, xmax = min(xList), max(xList)
                    ymin, ymax = min(yList), max(yList)
                    bbox = xmin, ymin, xmax, ymax
                    label = "Unknown"

                    # Check if the hand we are iterating upon is the right one.
                    if self.hands_status['Right_index'] == hand_index:

                        # Update the label and store the landmarks of the hand in the dictionary.
                        label = 'Right Hand'

                        # Check if the hand we are iterating upon is the left one.
                    elif self.hands_status['Left_index'] == hand_index:

                        # Update the label and store the landmarks of the hand in the dictionary.
                        label = 'Left Hand'

                if draw:
                    cv.rectangle(image,(xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
                    cv.putText(image, label, (xmin, ymin + 25), cv.FONT_HERSHEY_COMPLEX, 0.7, (20, 255, 155), 1, cv.LINE_AA)

        return self.lmList,bbox,self.hands_status

    def fingerUp(self):
        fingers = []
    # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] -1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] -2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        fingers.append(self.hands_status['Right'])
        fingers.append(self.hands_status['Left'])
    # totalFingers = fingers.count(1)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        '''if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (cx, cy), r, (0, 0, 255), cv.FILLED)
        '''
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    previousTime = 0
    currentTime = 0
    cap = cv.VideoCapture(1)
    detector = handDetector()

    while True:
        success, image = cap.read()
        image = detector.findHands(image)
        lmList, bbox = detector.findPosition(image)
        if len(lmList)!=0:
            print(lmList[4])

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv.putText(image, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv.imshow("Image", image)
        cv.waitKey(1)


if __name__ == '__main__':
    main()
