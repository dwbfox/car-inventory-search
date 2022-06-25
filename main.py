#!/usr/bin/env python3
'''Get dealer inventory listing and prices without the hassle'''

import argparse

from dealer import DealerInventory


def main():
    '''Main App entry point'''
    parser = argparse.ArgumentParser(
        description='dealer-inventory-check - '
        'Get dealer inventory listing and prices without the hassle.'
    )
    parser.add_argument('--dealer_url', required=True, metavar='dealer_url', type=str,
                        help='URL to the dealership homepage.')
    parser.add_argument('--sort', default='Model',
                        help='Sort the output table by a column')
    parser.add_argument('--output', default='table', choices=['csv', 'json', 'table'],
                        help='Format of the output, either csv, json, or table.')
    parser.add_argument('--condition', default='new', choices=['new', 'used'],
                        help='Condition of the vehicles, new or used.')
    args = parser.parse_args()

    query = {
        'condition': args.condition,
        'dealer_url': args.dealer_url
    }
    dealer = DealerInventory(query)
    if args.output == 'json':
        print(dealer.gen_json())
    elif args.output == 'csv':
        file_name = 'inventory.csv'
        print(f"Generated CSV as {file_name}.")
        dealer.gen_csv(file_name)
    elif args.output == 'table':
        print(dealer.gen_table())


if __name__ == '__main__':
    main()
