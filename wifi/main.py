#!/usr/bin/python
import hashlib
import os
from datetime import datetime

import pytz
import requests
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from scapy.all import *  # noqa: F403

CACHE_NAME = 'devices'
CACHE_OPTIONS = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock',
    'cache.expire': 10
}


IOT_AGENT_URL = os.getenv('IOT_AGENT_URL', 'http://localhost:7896')
IOT_AGENT_SERVICE_KEY = os.getenv(
    'IOT_AGENT_SERVICE_KEY',
    '4jggokgpepnvsb2uv4s40d59ov'
    )
IOT_AGENT_DEVICE = os.getenv('IOT_AGENT_DEVICE', 'sniffer001')


def send_measure(device, source, identifier, instant):
    URL = '%s/iot/d?k=%s&i=%s' % (IOT_AGENT_URL, IOT_AGENT_SERVICE_KEY, device)
    data = 'm|%s %s %s' % (source, identifier, instant)

    return requests.post(URL, data=data)


cache = CacheManager(**parse_cache_config_options(CACHE_OPTIONS))


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def handle_packet(packet):
    if not packet.haslayer(Dot11ProbeReq):  # noqa: F405
        return

    if packet.type != 0 or packet.subtype != 0x04:
        return

    hashed_mac = encrypt_string(packet.addr2)
    try:
        cache.get_cache(CACHE_NAME).get(hashed_mac)

    except Exception:
        pass

    else:
        # Already registered in cache
        return

    instant = pytz.UTC.localize(datetime.utcnow()).isoformat()
    send_measure(IOT_AGENT_DEVICE, 'wifi', hashed_mac, instant)

    cache.get_cache(CACHE_NAME).put(hashed_mac, 1)


def main():
    sniff(iface='mon0', prn=handle_packet, store=0)  # noqa: F405


if __name__ == '__main__':
    main()
