import argparse
from multiprocessing import Process

import cv2

from publisher import Publisher
from subscriber import Subscriber


def publisher():
    pub = Publisher()
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break
        pub.send(frame)
        cv2.imshow("Publisher", frame)

        key = cv2.waitKey(20)
        if key == 27:  # Esc
            break
        if cv2.getWindowProperty("Publisher", cv2.WND_PROP_VISIBLE) < 1:
            break
    pub.close()


def subscriber(name: str):
    sub = Subscriber()
    while True:
        _, frame = sub.recv()
        cv2.imshow(name, frame)

        key = cv2.waitKey(20)
        if key == 27:  # Esc
            break
        if cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) < 1:
            break
    sub.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=bool, default=False)
    parser.add_argument("-c", type=bool, default=False)
    parser.add_argument("-n", type=int, default=0)
    args = parser.parse_args()

    if args.s:
        Process(target=publisher).start()
    if args.c:
        Process(target=subscriber, args=(f'Subscriber {args.n}',)).start()
