import cv2
import numpy as np

# not necessary, just comment out
cv2.imshow('Map', cv2.imread('farmhouse-ground-floor.jpg'))

# if set to 0 = laptop webcam, 1 = camera
cap = cv2.VideoCapture(0)

while True:

    # Take each frame
    _, frame = cap.read()
    frame = cv2.medianBlur(frame, 5)
    cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    th = cv2.adaptiveThreshold(cimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 75, 1)
    # th = cv2.Canny(cimg, 50, 100)

    # Set up the detector with default parameters.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 500
    params.maxArea = 100000
    params.minDistBetweenBlobs = 10
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(th)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    frame_with_keypoints = cv2.drawKeypoints(th, keypoints, np.array([]), (0, 0, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show keypoints
    cv2.imshow("Keypoints", frame_with_keypoints)
    cv2.imshow("Source", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
