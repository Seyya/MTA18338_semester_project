import numpy as np
import cv2
import alexandria as alex

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frameToGrey = alex.rgb2grey(frame)
    showContours = alex.contouring(frameToGrey)

    #cv2.imshow("Greyscale", frameToGrey)
    cv2.imshow("Contours", showContours)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()
