

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
    width = 600
    height = 400
    drone = drone_control.Drone(width, height)

    #drone init for video
    drone.drone.set_loglevel(drone.drone.LOG_INFO)
    drone.drone.set_exposure(0)
    container = av.open(drone.drone.get_video_stream())
    count = 0
    frame_skip = 300

    # detection init
    detect = detection.Detection()

    try:
        #drone.start()
        while True:
            for frame in container.decode(video=0):
                # image from drone
                if 0 < frame_skip:
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
                plt.savefig("pic/" + str(count) + "_origin")
                img = detect.detection(image)
                # drone control
                # drone.follow_person(detect.bbox, detect.label, detect.score, 200*100)
                #cv2.waitKey(1)
                frame_skip = 300
                end_time = time.time() - start_time
                print ("{0}".format(end_time) + " [sec] ")
        drone.finish()
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        self.drone.quit()
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

def follow_person(bbox, label, score, threshold):
    area_sum = 0.0
    error_x = 0.0
    error_y = 0.0
    x_gain = 0.01
    y_gain = 0.01
    depth_gain = 0.01

    width = 600
    height = 400
    count_person = 0.0
    for i in range(len(bbox)):
        if label[i] == 14: #person
            area_sum += ((bbox[i][2] - bbox[i][0]) * (bbox[i][3] - bbox[i][1])) 
            error_x += ((bbox[i][1] + bbox[i][3] - width) / 2.0)
            error_y += ((bbox[i][0] + bbox[i][2] - height) / 2.0)
            count_person += 1.0
    area_ave = area_sum / count_person
    ave_error_x = error_x / count_person # x axis right
    ave_error_y = -1.0 * error_y / count_person # y axis  down:plt -> up:drone control

    control_x = 0.0
    control_y = 0.0
    control_depth = 0.0
    # depth control
    if area_sum > threshold:
        control_depth = depth_gain * (area_ave - threshold)
        print("backward {0}".format(control_depth))
    elif area_sum < threshold:
        control_depth = - depth_gain * (area_ave - threshold)
        print("forward {0}".format(control_depth))

    # x control
    if ave_error_x > 0:
        control_x = x_gain * ave_error_x
        print("right {0}".format(control_x))
    if ave_error_x < 0:
        control_x = - x_gain * ave_error_x
        print("left {0}".format(control_x))

    # y control
    if ave_error_y > 0:
        control_y = y_gain * ave_error_y
        print("up {0}".format(control_y))
    if ave_error_y < 0:
        control_y = - y_gain * ave_error_y
        print("down {0}".format(control_y))

if __name__ == '__main__':
    main()
    #test()
    
