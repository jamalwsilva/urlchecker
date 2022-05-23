#!/usr/bin/env python3

import ssl
import OpenSSL
from datetime import datetime
import json
import argparse
import sys
import socket
import logging

DEFAULT_TIMEOUT = 5
DEFAULT_PORT = 443
DEFAULT_DAYS_THRESHOLD = 5

def init_program_options():
    parser = argparse.ArgumentParser(description='Simple Domain Certificate Checker')
    parser.add_argument('--addresses', nargs='+', help='Address list to check (domain or subdomain)')
    parser.add_argument('--days-threshold', type=int, default=10, help='How many days in order to mark certificate with TO_EXPIRE flag')
    parser.add_argument('--default-port', type=int, default=443, help='Default TLS port')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    return parser.parse_args()


def request(address, default_port, days_threshold):
    conn = ssl.create_connection((address, default_port))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    sock = context.wrap_socket(conn, server_hostname=address)
    certificate = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    cname = x509.get_subject().commonName
    not_after = x509.get_notAfter().decode('utf-8')
    expire_date = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
    has_expired = x509.has_expired()
    diff = expire_date - datetime.now()
    to_expire = diff.total_seconds() / 86400 < days_threshold

    return {
        "hostname": address,
        "cname": cname,
        "not_after": expire_date.isoformat(),
        "has_expired": has_expired,
        "to_expire": to_expire,
    }


def request_urls(addresses, default_port, days_threshold):
    for address in addresses:
        try:
            yield request(address, default_port, days_threshold)    
        except Exception as error:
            logging.error(error)
            yield {
                "hostname": address,
                "error": True,
                "reason": str(error),
            }


def main():
    socket.setdefaulttimeout(DEFAULT_TIMEOUT)

    args = init_program_options()
    result = request_urls(args.addresses, args.default_port, args.days_threshold)
    for item in result:
        print(json.dumps(item))


if __name__ == '__main__':
    main()
