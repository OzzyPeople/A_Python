import json
import zlib
from datetime import datetime


def make_request(action, text, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'time': date.timestamp()
    }

# если идет режим записи

def write_mode(sock):
    action = input('Enter action name: ')
    message = input('Enter your message: ')
    request = make_request(action, message)
    string_request = json.dumps(request)
    bytes_request = string_request.encode()
    compressed_request = zlib.compress(bytes_request)
    response = sock.send(compressed_request)
    return response

def read_mode(sock, buffersize):
# если идет режим чтения
    compressed_response = sock.recv(buffersize)
    bytes_response = zlib.decompress(compressed_response)
    response = json.loads(bytes_response)
    print(compressed_response)
    print(response)