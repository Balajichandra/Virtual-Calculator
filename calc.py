#Note use cvzone version 1.5.3
import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        #drawing a box
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(255,255,255),cv2.FILLED)
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
        cv2.putText(img,self.value,(self.pos[0]+40,self.pos[1]+60),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)

    def checkclick(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.height:
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(255,255,255),cv2.FILLED)
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
            cv2.putText(img,self.value,(self.pos[0]+20,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
            return True
        else:
            return False    

#webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.9,maxHands=1)

#creating button
buttonlistvalues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['0','/','clr','=']]
buttonlist = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonlist.append(Button((xpos,ypos),100,100,buttonlistvalues[y][x]))

#creating equation
myEquation = ''
delay_counter = 0
while True:
    #get image from web cam
    success ,img = cap.read()
    img = cv2.flip(img,1)

    #detection of hands
    hands,img = detector.findHands(img,flipType=False)
    
    #draw result area
    cv2.rectangle(img,(800,70),(800+400,70+100),(255,255,255),cv2.FILLED)
    cv2.rectangle(img,(800,70),(800+400,70+100),(50,50,50),3)
    #draw all buttons
    for button in buttonlist:
        button.draw(img)
    
    #check for hands
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8],lmList[12],img)
        x,y = lmList[8]
        if length < 50 :
            for i,button in enumerate(buttonlist):
                if button.checkclick(x,y) and delay_counter == 0:
                    my_values = buttonlistvalues[int(i%4)][int(i/4)]
                    if my_values == "=":
                        myEquation = str(eval(myEquation))
                    else:    
                        myEquation+=my_values
                    if my_values == "clr":
                        myEquation = ''    
                    delay_counter = 1
    
    #Avoid duplicates
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0                    

    #put result
    cv2.putText(img,myEquation,(810,130),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)
    #display image
    cv2.imshow("Image",img)
    cv2.waitKey(1)