#!/usr/bin/env python

import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gateway-ip", required=True, help="IP address of the gateway machine.")
    parser.add_argument("-v", "--victim-ip", required=True, help="IP address of the victim machine.")
    parser.add_argument("-b", "--spoof-both", type=bool, help="Enable/disable bidirectional spoofing.")
    parser.add_argument("-c", "--count", type=int, help="The number of ARP packets to send. Defaults to 5. Use 0 to send ad infinitum.")
    parser.parse_args()

if __name__ == "__main__":
    main()