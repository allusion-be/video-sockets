import argparse
import pickle
import socket
import struct

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-sip", "--server-ip", type=str,
                    default="127.0.0.1", help="server ip")
parser.add_argument("-sp", "--server-port", type=int,
                    default=9999, help="server port")
args = parser.parse_args()

socket_addr = (args.server_ip, args.server_port)
with socket.socket() as s:
    print(f'[INFO] Listening to {socket_addr[0]}:{socket_addr[1]}.')
    s.connect(socket_addr)

    data, payload_size = b"", struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = s.recv(4*1024)
            if not packet:
                break
            data += packet

        packet_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packet_size)[0]
        while len(data) < msg_size:
            data += s.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Client", frame)

        key = cv2.waitKey(20)
        if key == 27:  # Esc
            break
        if cv2.getWindowProperty("Client", cv2.WND_PROP_VISIBLE) < 1:
            break
    s.close()
