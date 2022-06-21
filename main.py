#!/usr/bin/env python3

import argparse
from urllib.parse import urlsplit
from requests import get

from dealerplugins import (
     dealeron,
     dealertrack
)



def load_dealer_plugin(dealer_url):
    '''Try to detect the platform of the given dealer
    for correct parsing'''

    platforms = {
        'dealeron': dealeron,
        'dealertrack': dealertrack
    }
    res = get(dealer_url)
    if res.status_code != 200:
        raise Exception("Unable to determine the dealer platform. Maybe it's not supported")
    if 'dealertrack' in res.text.lower():
        platform = 'dealertrack'
    elif 'dealeron' in res.text.lower():
        platform = 'dealeron'
    return platforms[platform]

def main():
    '''Main entry point'''
    parser = argparse.ArgumentParser(description='dealer-inventory-check - Get dealer inventory listing and prices without the hassle.')
    parser.add_argument('--dealer_url', required=True, metavar='dealer_url', type=str,
                        help='URL to the dealership homepage.')
    parser.add_argument('--sort', default='Model',
                        help='Sort the output table by a column')
    parser.add_argument('--output', default='table', choices=['csv', 'json', 'table'],
                        help='Format of the output, either csv, json, or table.')
    args = parser.parse_args()
    dealer_plugin = load_dealer_plugin(args.dealer_url)

    
if __name__ == '__main__':
    main()