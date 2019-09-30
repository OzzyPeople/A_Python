import yaml
import json
import zlib
import socket
from argparse import ArgumentParser
from client_mode_response import write_mode, read_mode

READ_MODE = 'r'
WRITE_MODE = 'w'


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

    #два режима - чтение (полученных сообщений) или написание их
    #дефолт режиме - чтение
    parser.add_argument('-m', '--mode', type=str, default=READ_MODE,
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
        #пока клиент не будет закрыт
        while True:
            #если идет режим записи
            if args.mode == WRITE_MODE:
                write_mode(sock)
            # если идет режим чтения
            else:
                read_mode(sock, buffersize)
    except KeyboardInterrupt:
        print('Client shoutdown')