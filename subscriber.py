import numpy as np
import zmq


class Subscriber:
    def __init__(self, address='tcp://127.0.0.1', port=9999):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.socket.connect(f'{address}:{port}')

    def recv(self):
        metadata, message = self.socket.recv_json(), self.socket.recv(copy=False)
        a = np.frombuffer(message, dtype=metadata['dtype'])
        return metadata['msg'], a.reshape(metadata['shape'])

    def close(self):
        self.socket.close()
        self.context.term()
