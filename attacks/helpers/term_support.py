#!/usr/bin/env python


class headers:
    ERR = '\033[1;31;40m' + " [-] "
    SCS = '\033[1;32;40m' + " [+] "
    WRN = '\033[1;33;40m' + " [!] "
    INF = '\033[1;34;40m' + " [.] "
    QST = '\033[1;35;40m' + " [?] "
    REG = '\033[1;37;40m' + " [.] "
    ENDC = '\033[0m'


def pprint(message, status):
    print(status + message + headers.ENDC + "\n")
