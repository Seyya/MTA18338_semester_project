import cv2

import alexandria as al


def roi_boi(outline, img):  # should be given the outlines given by the second output of contours (contours[1])
    xarray = []
    yarray = []
    it = 0
    for i in range(len(outline)):  # outline contains multiple outlines (one set for each contour)
        salasa = str(it)
        it += 1
        for j in outline[i]:
            yarray.append(j.x)
            xarray.append(j.y)
        x = min(xarray)
        y = min(yarray)
        l = max(yarray)
        b = max(xarray)

        temp = img[y:l, x:b]  # from min to max (min:max)
        try:
            cv2.imshow(salasa, temp)
        except AssertionError:
            print('Error occurred. Probably safe to ignore')


cap = cv2.VideoCapture('Bouncing White Ball.mp4')
framecounter = 0

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    framecounter += 1
    if framecounter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        framecounter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (300, 300))
    gray = al.rgb2grey(frame)
    bi = al.binary_threshold(gray, 170)
    con = al.contouring(bi)
    # Display the resulting frame
    cv2.imshow('contours', con[0])
    roi_boi(con[1], frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
