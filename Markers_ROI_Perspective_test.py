import cv2

import alexandria as al

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    if capture.isOpened():  # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:
        # important stuff starts here
        frame = cv2.resize(frame, (200, 200))
        gray = al.rgb2grey(frame)
        bina = al.binary_threshold(gray, 127)
        conts, outlines = al.contouring(bina, 0)
        twat = al.roi_boi(outlines, bina)
        # stops here

        cv2.imshow('Test Frame', conts)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
