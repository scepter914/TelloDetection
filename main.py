

import drone
import detection

import cv2
import time

def main():
    # detection init
    detect = detection.Detection()
    # drone init
    # drone = drone.Drone()
    cap = cv2.VideoCapture('pic/hoge.mp4')
    while(cap.isOpened()):
        print("read pic")
        ret, frame = cap.read()
        start = time.time()
        img = detect.detection(frame)
        end_time = time.time() - start
        #bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #cv2.imshow("result", bgr)
        print ("{0}".format(end_time) + " [sec]")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    
