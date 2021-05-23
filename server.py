import argparse
import pickle
import socket
import struct

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=9999,
                    help="server socket port")
args = parser.parse_args()

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
socket_addr = (host_ip, args.port)
with socket.socket() as s:
    print(f'[INFO] Listening at {host_ip}:{socket_addr[1]}.')
    s.bind(socket_addr)
    s.listen(5)

    while True:
        c_socket, addr = s.accept()
        print(f'[INFO] Got connection from {addr}.')
        if c_socket:
            cam = cv2.VideoCapture(0)
            while cam.isOpened():
                ret, frame = cam.read()
                if not ret:
                    break

                a = pickle.dumps(frame)
                msg = struct.pack("Q", len(a)) + a
                c_socket.sendall(msg)
                cv2.imshow("Server", frame)

                key = cv2.waitKey(20)
                if key == 27:  # Esc
                    break
                if cv2.getWindowProperty("Server", cv2.WND_PROP_VISIBLE) < 1:
                    break
            c_socket.close()
    s.close()
