import numpy as np
import cv2

#Open image, convert to greyscale and blur
testImg = cv2.imread('Sheeps01.jpg', 0)
blur = cv2.GaussianBlur(testImg,(5,5),0)
__, binaryImg = cv2.threshold(testImg,127,255,cv2.THRESH_BINARY)
#cam = cv2.VideoCapture(0)
#ret, frame = cam.read()
#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def runGrassFire(id, location, treshMin, treshMax, sourceImg, result):
    height = sourceImg.shape[0]
    width = sourceImg.shape[1]
    #Create array for new locations to check
    newQueue = []
    #print("The location is: " + str(location))

    #Check pixel above
    y, x = location

    if y - 1 >= 0:
        if result[y -1, x] == 0:
            #If the pixel is within the treshold, assign ID and add to queue
            if sourceImg[y -1, x] >= treshMin and sourceImg[y - 1, x] <= treshMax:
                #print("Found pixel above.")

                result[y -1, x] = id
                newPosition = (y - 1, x)
                #Append the new location coordinates to the queue
                newQueue.append(newPosition)

    #Check pixel to the right
    if x + 1 < width:
        if result[y, x + 1] == 0:
            if sourceImg[y, x +1] >= treshMin and sourceImg[y, x + 1] <= treshMax:
                #print("Found pixel to the right")

                result[y, x +1] = id
                newPosition = (y, x +1)
                newQueue.append(newPosition)

    #Check pixel below
    if y + 1 < height:
        #print("The y-coordinate is: " + str(y))
        if result[y + 1, x] == 0:
            #print("The x and y coordinates are: " + str(y, x))
            if sourceImg[y + 1, x] >= treshMin and sourceImg[y + 1, x] <= treshMax:
                #print("Found pixel below")

                result[y + 1, x] = id
                newPosition = (y + 1, x)
                newQueue.append(newPosition)

    #check pixel to the left
    if x -1 >= 0:
        if result[y, x -1] == 0:
            if sourceImg[y, x -1] >= treshMin and sourceImg[y, x - 1] <= treshMax:
                #print("Found pixel to the left")

                result[y, x -1] = id
                newPosition = (y, x -1)
                newQueue.append(newPosition)

    #print("The new queue is: " + str(newQueue))
    return result, newQueue


def findBlob(sourceImg, treshMin, treshMax):
    #Create nesesary variables
    height = sourceImg.shape[0]
    width = sourceImg.shape[1]
    blobID = 1
    queue = []
    result = np.zeros(sourceImg.shape)

    #Loop through each pixel in the image
    for Ypos in range(0, width-1):
        for Xpos in range(0, height-1):
            #If the value of x and y is 0..
            if result[Xpos, Ypos] == 0:
                #.. check treshold..
                if sourceImg[Xpos, Ypos] >= treshMin and sourceImg[Xpos, Ypos] <= treshMax:
                    #.. and assign an id before running the grass-fire algorithm
                    #Overwrite the result and add the coordinates to the queue
                    sourceImg[Xpos, Ypos] = blobID
                    position = (Xpos, Ypos)
                    #print("The position is: " + str(position))
                    newResult, newQueue = runGrassFire(blobID, position, treshMin, treshMax, sourceImg, result)
                    result = newResult
                    queue.extend(newQueue)
                    #print("The current BLOB id is: " + str(blobID))

                    #As long as there is coordinates in the queue, keep running the grass-fire algorithm
                    while len(queue) != 0:
                        #print("The length of the queue is: " + str(len(queue)))
                        #print("This is the current queue: " + str(queue))
                        #print("The first element of the queue is: " + str(queue[0]))

                        #Take the first entry in the queue, run algorithm ect. before deleting the first entry in the queue
                        firstInQueue = queue[0]
                        newResult, newQueue = runGrassFire(blobID, firstInQueue, treshMin, treshMax, sourceImg, result)
                        result = newResult
                        queue.extend(newQueue)
                        del queue[0]
                        #print(str(len(queue)))
                    blobID += 1
    return result


a = findBlob(testImg, 0, 50)
cv2.imshow('Whatever', a)
cv2.imshow('Original', testImg)
#cv2.imshow('Feed', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
