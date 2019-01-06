
## TelloFollowingPerson

TelloFollowingPerson is application of drone following person.
This is a sample code of conection between TelloPy and detection algorthm sample of ChainerCV.

## !! Caution !!

- It is dangerous for a drone to fly automatically
- You can use this code at your own risk
    - Because of individual difference of drones, these codes always don't work well.
    - When your drone fly, you should check if anyone wasn't around the drone.

## OS and library version

- Ubuntu
    - Test by Ubuntu18.04LTS
- python3.6
- chainer==5.0.0
- chainercv==0.11.0
- Tellopy==0.6.0
    - <https://github.com/hanyazou/TelloPy>

## Installation

```

# General dependencies
sudo apt-get install -y python-dev pkg-config 

# Library components
sudo apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev

sudo pip3 install tellopy av opencv-python image chainer chainercv

```

- if error at installing pyav
    - <https://docs.mikeboers.com/pyav/develop/installation.html>

## Docs

- blog(Japanese)



