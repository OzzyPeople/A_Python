import json
import zlib
from datetime import datetime

#обработка вводимой информации пользователя
def make_request(action, text, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'time': date.timestamp()
    }

#читаем сообщения
def read_mode(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        bytes_response = zlib.decompress(compressed_response)
        response = json.loads(bytes_response)
        print(response)

#отправляем сообщения
def write_mode(sock, action, message):
    while True:
        request = make_request(action, message)
        string_request = json.dumps(request)
        bytes_request = string_request.encode()
        compressed_request = zlib.compress(bytes_request)
        response = sock.send(compressed_request)
        return response

