

import drone_control
import detection

import cv2
import time
import matplotlib.pyplot as plt
import tellopy

# video
import sys
import traceback
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy

def main():
    width = 1000
    height = 720
    drone = drone_control.Drone(width, height)

    #drone init for video
    drone.drone.set_loglevel(drone.drone.LOG_INFO)
    drone.drone.set_exposure(0)
    container = av.open(drone.drone.get_video_stream())
    count = 0
    frame_skip = 1000

    # detection init
    detect = detection.Detection()

    # start
    drone.start()

    try:
        for frame in container.decode(video=0):
            # image from drone
            if 0 < frame_skip and count < 6:
                frame_skip = frame_skip - 1
                continue
            count += 1
            start_time = time.time()
            image = numpy.array(frame.to_image())
            plt.imshow(image)
            #plt.show()
            #image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
            #cv2.imshow('Original', image)
            #cv2.imshow('Canny', cv2.Canny(image, 100, 200))
            #plt.savefig("pic/" + str(count) + "_origin")
            img = detect.detection(image)
            # drone control
            drone.follow_person(detect.bbox, detect.label, detect.score, 400*500)
            #cv2.waitKey(1)
            frame_skip = 300
            end_time = time.time() - start_time
            print ("{0}".format(end_time) + " [sec] ")
        drone.finish()
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        drone.drone.land()
        drone.drone.quit()
        print(ex)
    finally:
        cv2.destroyAllWindows()
    #drone.video_test()
    #drone.move_test(40)

def test_yolo():
    width = 600
    height = 400
    # detection init
    detect = detection.Detection()
    cap = cv2.VideoCapture('pic/hoge.mp4')
    while(cap.isOpened()):
        # detection
        ret, frame = cap.read()
        frame = cv2.resize(frame, (width, height))
        start = time.time()
        img = detect.detection(frame)
        follow_person(detect.bbox, detect.label, detect.score, 200*100)
        #bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #cv2.imshow("result", bgr)
        end_time = time.time() - start
        print ("frame {0}:  {1}".format(detect.count, end_time) + " [sec]")
        print()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    #test()
    
