import cv2
import time
import math
import mediapipe as mp

class handDetector:
    def __init__(self, mode=False, max_hands=2, modelComp=1, det_conf=0.5, track_conf=0.5):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, max_hands, modelComp, det_conf, track_conf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True, w_width=640, h_height=480):

        img = cv2.resize(img, (w_width, h_height))
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handlms, self.mpHands.HAND_CONNECTIONS,                                           # We used img here as we need to draw on img not img_RGB
                        landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(                          # Specifies drawing properties for landmarks
                            color=(255, 0, 0), thickness=4, circle_radius=2),                                  # color is taken as RGB (as we have converted to RGB)
                        connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(                        # Specifies drawing properties for connections
                            color=(0, 0, 255), thickness=2, circle_radius=2)                                   # Thickness and Circle_Radius to be int values
                    )
        return img

    def findPos(self, handNo=0, w_width=640, h_height=480):

        self.lmlist = []
        if self.results.multi_hand_landmarks and handNo < len(self.results.multi_hand_landmarks):
            handlms = self.results.multi_hand_landmarks[handNo]
            self.lmlist = [[id, int(lm.x * w_width), int(lm.y * h_height)] for id, lm in enumerate(handlms.landmark)]     # List comprehension for faster extraction
        return self.lmlist
    
    def fingUp(self):
        
        finger_tip_ids = [8,12,16,20]
        if len(self.lmlist)!=0 :            # Shape of lmlist is 2D List, [[id,cx,cy],[...],....,[...]]
            fing_count = []                 # A list which contains which finger is up
            for i in range(4):
                if (self.lmlist[finger_tip_ids[i]][2] < self.lmlist[finger_tip_ids[i]-2][2]):       # We only need fingers up/down data not the thumb
                    fing_count.append(1)
                else:
                    fing_count.append(0)
            return fing_count
        
# Jab image par draw karna ho toh ya toh usko RGB me rakho and phir cv2.imshow ke time se pehle BGR me convert kardo ya phir seedha BGR image par hi draw kardo