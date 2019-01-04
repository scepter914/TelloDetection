
from time import sleep
import tellopy

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

    def __init__(self):
        self.drone = tellopy.Tello()

    def drone_test():
        try:
            self.drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
            self.drone.connect()
            self.drone.wait_for_connection(60.0)
            self.drone.takeoff()
            sleep(5)
            self.drone.down(50)
            sleep(5)
            self.drone.land()
            sleep(5)
        except Exception as ex:
            print(ex)
        finally:
            self.drone.quit()

    def video_test():
        try:
            drone.connect()
            drone.wait_for_connection(60.0)

            container = av.open(drone.get_video_stream())
            # skip first 300 frames
            frame_skip = 300
            while True:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue
                    start_time = time.time()
                    image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    cv2.imshow('Original', image)
                    cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                    cv2.waitKey(1)
                    frame_skip = int((time.time() - start_time)/frame.time_base)

        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            drone.quit()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    drone = Drone()
    drone_test()
