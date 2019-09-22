#!/usr/bin/python
import hashlib
import os
from datetime import datetime

import pytz
import requests
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from bluetooth.ble import DiscoveryService
from multiprocessing import Pool

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


def handle_packet(mac_address):
    mac_address = mac_address.lower()
    hashed_mac = encrypt_string(mac_address)
    try:
        cache.get_cache(CACHE_NAME).get(hashed_mac)

    except Exception:
        pass

    else:
        # Already registered in cache
        return

    instant = pytz.UTC.localize(datetime.utcnow()).isoformat()
    send_measure(IOT_AGENT_DEVICE, 'bluetooth-ble', hashed_mac, instant)

    cache.get_cache(CACHE_NAME).put(hashed_mac, 1)


def main():
    pool = Pool(processes=1)

    while True:

        svc = DiscoveryService()
        devs = svc.discover(5)

        if devs:
            for addr, _ in devs.items():
                pool.apply_async(handle_packet, [addr])            


if __name__ == '__main__':
    main()
