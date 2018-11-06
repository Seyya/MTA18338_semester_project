import numpy as np
import cv2

#video capture
cv2.namedWindow("preview")
cam = cv2.VideoCapture(0)
img_counter = 0

# Set up the matrix for the filter - kernel
gauss = (1.0 / 57) * np.array(
    [[0, 1, 2, 1, 0],
     [1, 3, 5, 3, 1],
     [2, 5, 9, 5, 2],
     [1, 3, 5, 3, 1],
     [0, 1, 2, 1, 0]])
sum(sum(gauss))


def calcBlur(sourceImg, sourceKernel):
    # Get height and width
    height = sourceImg.shape[0]
    width = sourceImg.shape[1]
    result = np.zeros(sourceImg.shape, dtype=np.uint8)

    # computate everything!
    for sourceY in np.arange(2, height - 2):
        for sourceX in np.arange(2, width - 2):
            subResult = 0.0
            for kernelY in np.arange(-2, 3):
                for kernelX in np.arange(-2, 3):
                    a = sourceImg.item(sourceY + kernelY, sourceX + kernelX)
                    p = sourceKernel[2 + kernelY, 2 + kernelX]
                    subResult = subResult + (p * a)
            b = subResult
            result.itemset((sourceY, sourceX), b)
    return result


#Control the camera feed, press t to take a snapshot and apply the math
while True:
    ret, frame = cam.read()
    cv2.imshow('Source', frame)
    H = frame.shape[0]
    W = frame.shape[1]
    if not ret:
        break
    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break
    elif k & 0xFF == ord('t'):
        testResult = calcBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), gauss)
        cv2.imshow('Result', testResult)


cv2.waitKey(0)
cv2.destroyAllWindows()