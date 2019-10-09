#!/usr/bin/env python

import win32serviceutil
import time
import sys
from .term_support import pprint, headers


class WService:

    def __init__(self, service, machine=None, verbose=False):
        self.service = service
        self.machine = machine
        self.verbose = verbose

    @property
    def running(self):
        return win32serviceutil.QueryServiceStatus(self.service)[1] == 4

    def start(self):
        if not self.running:
            win32serviceutil.StartService(self.service)
            time.sleep(1)
            if self.running:
                if self.verbose:
                    pprint(
                        f"{self.service} started successfully.",
                        headers.SCS
                    )
                return True
            else:
                if self.verbose:
                    pprint(
                        f"Cannot start {self.service}",
                        headers.ERR
                    )
                return False
        elif self.verbose:
            pprint(
                f"{self.service} is already running.",
                headers.WRN
            )

    def stop(self):
        if self.running:
            win32serviceutil.StopService(self.service)
            time.sleep(0.5)
            if not self.running:
                if self.verbose:
                    pprint(
                        f"{self.service} stopped successfully.",
                        headers.SCS
                    )
                return True
            else:
                if self.verbose:
                    pprint(
                        f"Cannot stop {self.service}",
                        headers.ERR
                    )
                return False
        elif self.verbose:
            pprint(
                f"{self.service} is not running.",
                headers.WRN
            )

    def restart(self):
        if self.running:
            win32serviceutil.RestartService(self.service)
            time.sleep(2)
            if self.running:
                if self.verbose:
                    pprint(
                        f"{self.service} restarted successfully.",
                        headers.SCS
                    )
                return True
            else:
                if self.verbose:
                    pprint(
                        f"Cannot start {self.service}",
                        headers.ERR
                    )
                return False
        elif self.verbose:
            pprint(
                f"{self.service} is not running.",
                headers.WRN
            )


def main(action, service):
    service = WService(service, verbose=True)
    if action == "start":
        service.start()
    elif action == "stop":
        service.stop()
    elif action == "restart":
        service.restart()


def usage():
    print('''
  Usage: win_service.py [SERVICE] [ACTION]
    SERVICE : Name of the service to enable
    ACTION  : Specified action; either "start", "stop", or "restart"''')


if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        exit()

    main(sys.argv[2], sys.argv[1])
