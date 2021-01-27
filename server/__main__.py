import yaml
import socket
import select
import logging
import threading
from argparse import ArgumentParser

from resolvers import find_server_action
from handlers import handle_tcp_request


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

#конфигурация всех логеров для уровней, хэндлеров, форматеров
#не создаем logging.logger так как он есть по умолчанию в модуле logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)
#так как у нас может быть до 5 одновременно клиентов, делаем списки запросов и подключений
requests = []
connections = []

#чтение сокетов
def read(sock, requests, buffersize):
    bytes_request = sock.recv(buffersize)
    if bytes_request: #если есть байты
        requests.append(bytes_request)

#отправка сообщений через сокеты
def write(sock, response):
    sock.send(response)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.setblocking(0)
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()

    while True:
        try:
            client, (client_host, client_port)  = sock.accept()
            logging.info(f'Client {client_host}:{client_port} was connected')
            connections.append(client)
        # любое исключение
        except:
            pass
        # реализация блока - неблокирующего сервера - функция select, timeout = 0
        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )
        # формируем перечень пользовательских запросов
        for read_client in rlist:
            #добавляем многопоточность и аргументы read - функция и аргументы ее
            read_thread = threading.Thread(target=read, args=(read_client, requests, buffersize)) #байтовые запросы
            #запускаем функцию на выполнение в потоке
            read_thread.start()

        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_tcp_request(bytes_request, action_mapping)

            for write_client in wlist:
                # добавляем многопоточность и аргументы write - функция и аргументы ее
                write_thread =  threading.Thread(target=write, args=(write_client, bytes_response))
                # запускаем функцию на выполнение в потоке
                write_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown')
