# 与核心C服务进行ZeroMQ通信的服务
import zmq

def receive_message_from_core():
    context = zmq.Context()
    # 使用PULL套接字接收消息
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")  # 更改为适合您的端口和地址

    while True:
        message = socket.recv_string()
        process_message(message)

def process_message(message):
    # 对接收到的消息进行处理
    pass
