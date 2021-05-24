import numpy as np
import zmq


class Publisher:
    def __init__(self, address='tcp://127.0.0.1', port=9999):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f'{address}:{port}')

    def send(self, a: np.ndarray, msg: str = ''):
        self.socket.send_json(dict(
            msg=msg,
            dtype=str(a.dtype),
            shape=a.shape,
        ), zmq.SNDMORE)
        return self.socket.send(a)

    def recv(self):
        metadata, message = self.socket.recv_json(), self.socket.recv()
        a = np.frombuffer(message, dtype=metadata['dtype'])
        return metadata['msg'], a.reshape(metadata['shape'])

    def close(self):
        self.socket.close()
        self.context.term()
