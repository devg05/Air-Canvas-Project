import cv2
import numpy as np
import mediapipe as mp
import HandDetect as hd

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def generate_frames():
    
    def nothing(q):
        pass

    # For screenshot gesture part train own model and predict the frame having that gesture

    def create_canvas():
        temp = np.zeros((720,1100,3),dtype='uint8')                                                # see that size of webcam is 1100*720 so we initialise paintW with rows = 720
        paintW = np.zeros((720,1100,3),dtype='uint8')+255
        paintW = cv2.rectangle(paintW, (40,1),  (160,90), (0,0,0), 2)
        paintW = cv2.rectangle(paintW, (190,1), (310,90), (255,0,0), 2)
        paintW = cv2.rectangle(paintW, (340,1), (460,90), (0,255,0), 2)
        paintW = cv2.rectangle(paintW, (490,1), (610,90), (0,0,255), 2)
        paintW = cv2.rectangle(paintW, (640,1), (760,90), (255,0,255), 2)
        paintW = cv2.rectangle(paintW, (790,1), (910,90), (0,255,255), 2)
        paintW = cv2.rectangle(paintW, (940,1), (1060,90),(50,50,50), 2)
        cv2.putText(paintW, "CLEAR",  (75, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "BLUE",  (230, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "GREEN", (375, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "RED",   (535, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "PINK",  (680, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "YELLOW",(820, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintW, "ERASE", (975, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        return temp,paintW

    cap = cv2.VideoCapture(0)                                                                         # this always returns array with order col*rows and not rows*col
    det = hd.handDetector(det_conf = 0.45)
    w, h = 1100, 720                                                                                  # represents col & rows
    snap_ct=0
    draw_color = [(255,0,0),  (0,255,0),  (0,0,255),  (255,0,255), (0,255,255), (0,0,0)]
    color_ind = 0

    temp, paintW = create_canvas()
    cv2.namedWindow('Canvas')
    cv2.createTrackbar('Brush Size', 'Canvas', 5, 20, nothing)

    xp, yp = 0,0
    while True:
        _,img = cap.read()
        img = cv2.flip(img,1)
        img = det.findHands(img, False,w, h)
        lmlist = det.findPos(0,w,h)
        fing_up = det.fingUp()

        if (len(lmlist)!=0):
            x1,y1 = lmlist[8][1],lmlist[8][2]       # coordinates of index finger
            x2,y2 = lmlist[12][1], lmlist[12][2]    # coordinates of middle finger

            if (fing_up[0]==1 and fing_up[1]==1):
                xp,yp = x1,y1
                if y1 < 90:
                    if 40 < x1 < 160:       
                        temp, paintW = create_canvas()
                    elif 190 < x1 < 310:
                        color_ind = 0
                    elif 340 < x1 < 460:
                        color_ind = 1
                    elif 490 < x1 < 610:
                        color_ind = 2
                    elif 640 < x1 < 760:
                        color_ind = 3
                    elif 790 < x1 < 910:
                        color_ind = 4
                    elif 940 < x1 < 1060:
                        color_ind = 5

            elif (fing_up[0]==1 and fing_up[1]!=1):
                brush_thickness = cv2.getTrackbarPos('Brush Size', 'Canvas')

                if color_ind == 5:
                    cv2.circle(img, (x1, y1), 10, (255,255,255), 10)
                else: 
                    cv2.circle(img, (x1, y1), 10, draw_color[color_ind], 10)         # pass img, string to pe printed, location, font type, font size, font color & font thickn.

                if xp==0 and yp==0:
                    xp,yp = x1,y1
                
                if yp > 98:
                    if color_ind != 5:
                        cv2.line(img,   (xp,yp), (x1,y1), draw_color[color_ind], brush_thickness)
                        cv2.line(paintW,(xp,yp), (x1,y1), draw_color[color_ind], brush_thickness)
                        cv2.line(temp,  (xp,yp), (x1,y1), draw_color[color_ind], brush_thickness)
                    else:
                        cv2.line(paintW,(xp,yp), (x1,y1), (255,255,255), brush_thickness+5)
                        cv2.line(temp,  (xp,yp), (x1,y1), draw_color[color_ind], brush_thickness+5)
                xp,yp = x1,y1

            elif (fing_up[0]!=1 and fing_up[1]!=1):
                xp,yp = x1,y1

        img_gray = cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
        _,img_inv = cv2.threshold(img_gray,25,255,cv2.THRESH_BINARY_INV)            # If the pixel value > 25, it will be set to 0 (black) else it will be set to 255
        img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,img_inv)
        img = cv2.bitwise_or(img,temp)

        img = cv2.rectangle(img, (40,1),  (160,90), (0,0,0), 2)
        img = cv2.rectangle(img, (190,1), (310,90), (255,0,0), 2)
        img = cv2.rectangle(img, (340,1), (460,90), (0,255,0), 2)
        img = cv2.rectangle(img, (490,1), (610,90), (0,0,255), 2)
        img = cv2.rectangle(img, (640,1), (760,90), (255,0,255), 2)
        img = cv2.rectangle(img, (790,1), (910,90), (0,255,255), 2)
        img = cv2.rectangle(img, (940,1), (1060,90),(50,50,50), 2)
        cv2.putText(img, "CLEAR",  (75, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "BLUE",  (230, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "GREEN", (375, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "RED",   (535, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "PINK",  (680, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "YELLOW",(820, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "ERASE", (975, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # cv2.imshow('Webcam', img)
        # cv2.imshow('Canvas', paintW) 
        all_frames = np.hstack((img, paintW))
        ret, buffer = cv2.imencode('.jpg', all_frames)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()