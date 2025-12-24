import cv2
import numpy as np


CRACK_MIN_LENGTH = 30
BLOCK_AREA_THRESHOLD = 1000 

# url='http://10.130.239.236:81 /stream'

# cap = cv2.VideoCapture(url)
cap=cv2.VideoCapture(0)
cv2.namedWindow("Pipe Inspection", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("Pipe Inspection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while True:    
    ret, frame = cap.read()
    if not ret:
        print("Cam failed")
        break

    #frame = cv2.resize(frame, (640, 480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50,
                            minLineLength=CRACK_MIN_LENGTH, maxLineGap=5)

    crack_detected = False
    if lines is not None:
        crack_detected = True
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    block_detected = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > BLOCK_AREA_THRESHOLD:
            block_detected = True
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 
    framee=cv2.flip(frame,1)         

    
    if crack_detected:
        cv2.putText(framee, "Crack Detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (2200, 0, 50), 2)
        

    if block_detected:
        cv2.putText(framee, "Block Detected", (350, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)
        
    
    cv2.imshow("Pipe Inspection", framee)
    key = cv2.waitKey(1)
    if key==ord('s'):
        break




cap.release()
cv2.destroyAllWindows()
