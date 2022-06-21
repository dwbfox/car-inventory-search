#!/usr/bin/env python3

from re import search
from urllib.parse import urlsplit

import pandas as pd
from requests import get, JSONDecodeError


class DealerInventoryExeption(Exception):
    '''DealerInventoryExeption exception'''

class DealerInventory:
    ''' Provides mechanisms to interact with some front-end
        JSON objects provided _publicly_ by dealer websites to 
        centralize the information already available on dealer sites.
    '''

    def __init__(self, dealer_url):
        pd.set_option('display.max_colwidth', None)
        pd.set_option("display.max_rows", 100)
        self.vehicles = []
        self.data_frame = None
        self.dealer_url = urlsplit(dealer_url)
        self.endpoint = (
            '/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory'
        )
        self.api_url = f"{self.dealer_url.scheme}://{self.dealer_url.netloc}{self.endpoint}"
        print('API: ' + self.api_url)
        self.parse_dealer_inventory()


    def parse_dealer_inventory(self):
        '''Fetches a JSON string from provided dealer website and parses it 
        for easier consumption'''
        res = get(self.api_url)
        if res.status_code != 200:
            raise (
                DealerInventoryExeption(
                    "Failed to fetch inventory JSON from website. Maybe it's not compatible"
                )
            )
        try:
            self.dealer_inventory = res.json()['inventory']
        except JSONDecodeError as err:
            raise (
                DealerInventoryExeption(
                    "Failed to fetch inventory JSON from website. Maybe it's not compatible"
                )
            ) from err
        for item in self.dealer_inventory:
            vehicle = {}
            try:
                vehicle['Model'] = item['model']
                # Get detailed pricing breakdown
                vehicle['MSRP'] = (
                    [ i['value'] for i in item['pricing']['dPrice'] if i['label'].lower().startswith('msrp') ]
                )
                vehicle['Retail Price'] = [ item['pricing']['retailPrice'] if 'retailPrice' in item['pricing'] else 'Unknown' ]
                vehicle['Markup'] = (
                    [ i["value"] for i in  item['pricing']['dPrice']  if  search('.*option|installed|addendum|markup|fee.*', i["label"].lower()) ]
                )
                # Get detailed vehicle attributes
                vehicle['Stock Status'] = (
                    [ i["labeledValue"] for i in item['attributes'] if "vehiclestatus" in i["name"].lower() ]
                )
                vehicle['Stock Number'] = (
                    [ i["value"] for i in item['attributes'] if i["name"].lower() == "stocknumber" ]
                )
                vehicle['VIN'] = (
                    [ i["value"] for i in  item['attributes'] if i["name"].lower() == "vin" ]
                )    
                vehicle['url'] = f"{self.dealer_url.scheme}://{self.dealer_url.netloc}{item['link']}"
                self.vehicles.append(vehicle)
            except KeyError:
                # Assume no pricing data available
                continue

        self.data_frame = pd.DataFrame(self.vehicles)
        self.data_frame.sort_values(by='Retail Price', ascending=True)

    def gen_json(self):
        '''Returns a JSON string with the full 
        dealer inventory structure'''
        return self.dealer_inventory
 
    def gen_csv(self, file_name: str):
        '''Generates a CSV file with fetched inventory
        information to the specified file name'''
        return self.data_frame.to_csv(file_name)

    def gen_table(self, sort_column='Retail Price', ascending=True):
        '''Generates a formatted table output for direct
        consumption on the terminal'''
        return self.data_frame.from_dict(self.vehicles)