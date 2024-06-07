import cv2
from cvzone.HandTrackingModule import HandDetector

from time import sleep
from pynput.keyboard import Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = HandDetector(detectionCon=0.8, maxHands=2)


buttonList = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"," "],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";","&"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/","_"]]

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    def drawALL(self, img):  
        x , y = self.pos
        w , h = self.size
        cv2.rectangle(img , self.pos , ( x + w , y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text , ( x + 20 , y + 65 ),
                 cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img



               
        

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button((100 * j + 50, 100 * i + 50), key))
        
lmList1 = []
lmList2 = []
       
        
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img)
    #hands = detector.findHands(img, draw=False , flipType=False)
    # print(len(hands))     shows how many hands
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"] 
        fingers1 = detector.fingersUp(hand1)
        
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"] 
            fingers2 = detector.fingersUp(hand2)
    for obj in buttonList:
        img = obj.drawALL(img)
    if lmList1 :
        for obj in buttonList:
            x, y = obj.pos
            w, h = obj.size

            if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                cv2.rectangle(img, obj.pos , (x + w , y + h ), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, obj.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance((lmList1[8][0], lmList1[8][1]),(lmList1[4][0], lmList1[4][1]),)
               

                ## when clicked
                if l < 30:
                    cv2.rectangle(img, obj.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, obj.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    keyboard.press(obj.text)
                    sleep(0.3)
    


    
    cv2.imshow('image', img)
    cv2.waitKey(2)
    
