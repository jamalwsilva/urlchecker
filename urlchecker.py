#!/usr/bin/env python3

import ssl
import OpenSSL
from datetime import datetime
import json
import argparse
import sys


def init_program_options():
    parser = argparse.ArgumentParser(description='Simple Domain Certificate Checker')
    parser.add_argument('--addresses', nargs='+', help='Address list to check (domain or subdomain)')
    parser.add_argument('--days-thresold', type=int, default=3, help='How many days in order to mark certificate with TO_EXPIRE flag')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    return parser.parse_args()


def print_result(args):
    cert = ssl.get_server_certificate(('cajuzinho.com.br', 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

    cname = x509.get_subject().commonName
    not_after = x509.get_notAfter().decode('utf-8')
    expire_date = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
    has_expired = x509.has_expired()
    diff = expire_date - datetime.now()

    obj = {
        "cname": cname,
        "not_after": datetime_date.isoformat(),
        "has_expire": has_expired,
    }

    print(json.dumps(obj))


def main():
    args = init_program_options()
    print_result(args)


if __name__ == '__main__':
    main()