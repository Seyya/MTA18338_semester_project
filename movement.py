import cv2

cap = cv2.VideoCapture(0)
min_item_size = 200
firstFrame = None
lastFrame = None
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    h, w, layers = frame.shape
    nh = int(h / 2)
    nw = int(w / 2)
    # Frameoperations
    frame = cv2.resize(frame, (nw, nh))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)

    cunts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cunts = cunts[1]
    ID = 0
    for c in cunts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_item_size:
            continue

        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = 'My ID is: %s' % ID
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        ID += 1

    # Display frame
    cv2.imshow('Thrash', thresh)
    cv2.imshow('Delta', frameDelta)
    cv2.imshow('First Frame', firstFrame)
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        firstFrame = lastFrame
    lastFrame = gray

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
