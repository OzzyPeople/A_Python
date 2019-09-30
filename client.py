import yaml
import threading
import socket
from argparse import ArgumentParser
from client_mode_response import write_mode, read_mode


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024,
    }
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=False,
                        help='Sets config path')
    parser.add_argument('-ht', '--host', type=str, required=False,
                        help='Sets server host')
    parser.add_argument('-p', '--port', type=str, required=False,
                        help='Sets server port')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as file:
            file_config = yaml.safe_load(file)
            config.update(file_config or {})
    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    #чтобы процесс закрытия клиента не приводил к keboardinterrupt
    try:
        sock = socket.socket()
        sock.connect((host, port))

        #реализуем многопоточность чтения сообщений
        read_thread = threading.Thread(target=read_mode, args=(sock, buffersize))
        read_thread.start()

        while True:
            action = input('Enter action name: ')
            message = input('Enter your message: ')

            #реализуем многопоточность отправки сообщений
            write_thread = threading.Thread(target=write_mode, args=(sock, action, message))
            write_thread.start()

    except KeyboardInterrupt:
        print('Client shoutdown')