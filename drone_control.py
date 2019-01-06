
from time import sleep
import tellopy
import matplotlib.pyplot as plt

# video
import sys
import traceback
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

class Drone():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drone = tellopy.Tello()
        self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, handler)
        self.drone.connect()
        self.drone.wait_for_connection(60.0)
        #container = av.open(drone.get_video_stream())

    # start
    def start(self):
        try:
            self.drone.takeoff()
        except Exception as ex:
            self.drone.land()
            self.drone.quit()
            print(ex)

    # finish
    def finish(self):
        try:
            self.drone.land()
        except Exception as ex:
            self.drone.land()
            self.drone.quit()
            print(ex)
        finally:
            self.drone.quit()

    # move
    def follow_person(self, bbox, label, score, threshold):
        try:
            area_sum = 0.0
            error_x = 0.0
            error_y = 0.0
            x_gain = 0.09
            y_gain = 0.05
            depth_gain = 0.0001

            count_person = 0.0
            for i in range(len(bbox)):
                if label[i] == 14: #person
                    area_sum += ((bbox[i][2] - bbox[i][0]) * (bbox[i][3] - bbox[i][1])) 
                    error_x += ((bbox[i][1] + bbox[i][3] - self.width) / 2.0)
                    error_y += ((bbox[i][0] + bbox[i][2] - self.height) / 2.0)
                    count_person += 1.0
            if count_person < 0.5:
                #self.drone.quit()
                print("no person")
            else:
                area_ave = area_sum / count_person
                print(area_ave)
                ave_error_x = error_x / count_person # x axis right
                ave_error_y = -1.0 * error_y / count_person # y axis  down:plt -> up:drone control
                control_x = 0.0
                control_y = 0.0
                control_depth = 0.0
                # depth control
                if area_sum > threshold:
                    control_depth = depth_gain * (area_ave - threshold)
                    self.drone.backward(int(control_depth))
                    print("backward {0}".format(control_depth))
                elif area_sum < threshold:
                    control_depth = - depth_gain * (area_ave - threshold)
                    self.drone.forward(int(control_depth))
                    print("forward {0}".format(control_depth))

                # x control
                if ave_error_x > 0:
                    control_x = x_gain * ave_error_x
                    self.drone.right(int(control_x))
                    print("right {0}".format(control_x))
                if ave_error_x < 0:
                    control_x = - x_gain * ave_error_x
                    self.drone.left(int(control_x))
                    print("left {0}".format(control_x))

                # y control
                if ave_error_y > 0:
                    control_y = y_gain * ave_error_y
                    self.drone.up(int(control_y))
                    print("up {0}".format(control_y))
                if ave_error_y < 0:
                    control_y = - y_gain * ave_error_y
                    self.drone.down(int(control_y))
                    print("down {0}".format(control_y))
        except Exception as ex:
            self.drone.land()
            self.drone.quit()
            print(ex)

    def move_test(self, value):
        try:
            sleep(5)
            #self.drone.down(value)
            self.drone.forward(value)
            sleep(1)
        except Exception as ex:
            self.drone.land()
            self.drone.quit()
            print(ex)

    def video_test(self):
        try:
            self.drone.set_loglevel(self.drone.LOG_INFO)
            self.drone.set_exposure(0)
            #drone.connect()
            container = av.open(self.drone.get_video_stream())
            count = 0
            frame_skip = 300
            while True:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue
                    count += 1
                    start_time = time.time()
                    image = numpy.array(frame.to_image())
                    plt.imshow(image)
                    #plt.show()
                    plt.savefig("pic/" + str(count))

                    #image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    #cv2.imshow('Original', image)
                    #cv2.imshow('Canny', cv2.Canny(image, 100, 200))

                    cv2.waitKey(1)
                    #frame_skip = int((time.time() - start_time)/frame.time_base)
                    frame_skip = 300

        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            self.drone.quit()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    drone = Drone()
    drone.move_test()

