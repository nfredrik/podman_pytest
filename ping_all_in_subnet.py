import ping3
from scapy.all import sr1
from scapy.layers.inet import ICMP, IP


def ping_addr(ipaddr: str) -> str:
    """Ping an IP address using scapy."""
    packet = IP(dst=ipaddr)/ICMP()
    response = sr1(packet, timeout=2, verbose=False)

    if response:
        return f"🟢 {ipaddr} is reachable"
    else:
        return f"🔴 {ipaddr} is not reachable"


def hping_addr(ipaddr: str) -> str:
    """Ping addrs using ping3"""


    ping3.send_one_ping
    return ping3.verbose_ping(ipaddr)

if __name__ == "__main__":
    print(hping_addr("192.168.86.255"))



