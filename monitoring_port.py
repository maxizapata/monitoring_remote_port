import socket
import logging
from sys import argv
from time import sleep
from os import getcwd

# Config logging file
date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"
log_file = 'check_port.log'
logging.basicConfig(filename=f'{getcwd()}/{log_file}',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=message_format,
                    datefmt=date_strftime_format)


class MonitoringPort:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.is_alive = False
        self.first_time = True

    def check_remote_port(self):
        print(f'Monitoring ip {self.ip} on port {self.port}. \nSee {getcwd()}/{log_file} for details')
        logging.info(f'Monitoring ip {self.ip} on port {self.port}')
        while True:
            try:
                sleep(1)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                rc = sock.connect_ex((self.ip, self.port))
                if rc == 0:
                    if not self.is_alive:
                        logging.info(f'OK: {self.ip}:{self.port} is up')
                        self.is_alive = True
                else:
                    if self.is_alive or self.first_time:
                        logging.info(f'FAIL: {self.ip}:{self.port} is down')
                        self.is_alive = False
                        self.first_time = False
            except KeyboardInterrupt:
                print('Interrupcion')
                logging.info(f'It stopped monitoring {self.ip}:{self.port}')
                exit(0)


if __name__ == '__main__':
    mp = MonitoringPort(argv[1], int(argv[2]))
    mp.check_remote_port()
