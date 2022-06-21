# car-inventory-search

A small utility that gets publicly available inventory information from a provided car dealer URL
and provides a formatted table to ease car searching. It' currently limited to certain dealer inventory platforms,
so your mileage may vary when on the functionality of the script. May expand it to more dealer platforms in the future.

---

## Installation

### Install required Python dependencies
```bash
pip install -r requirements.txt
```

### Run
```bash
./main.py --dealer_url https://www.toyotaofgrapevine.com
```

### Output:
```
                Model       MSRP Retail Price Markup (Addendum)      Stock Status Stock Number VIN                                                                                                              url
0             Corolla  [$22,936]      $22,936                []  [DEALER ORDERED]           []  []            https://www.toyotaofgrapevine.com/new/Toyota/2022-Toyota-Corolla-82d2f86a0a0e0a9406d5b3e591208b9c.htm
1             Corolla  [$22,936]      $22,936                []  [DEALER ORDERED]           []  []            https://www.toyotaofgrapevine.com/new/Toyota/2022-Toyota-Corolla-82d3083a0a0e0a9406d5b3e50631263d.htm
2   Corolla Hatchback  [$24,326]      $24,326                []  [DEALER ORDERED]           []  []  https://www.toyotaofgrapevine.com/new/Toyota/2022-Toyota-Corolla+Hatchback-63e3874f0a0e0a936e1312378713064f.htm
3             Corolla  [$24,519]      $24,519                []  [DEALER ORDERED]           []  []            https://www.toyotaofgrapevine.com/new/Toyota/2022-Toyota-Corolla-62bad88e0a0e081d1c650a9bf7e19392.htm
4   Corolla Hatchback  [$24,701]      $24,701                []  [DEALER ORDERED]           []  []  https://www.toyotaofgrapevine.com/new/Toyota/2022-Toyota-Corolla+Hatchback-82d32d4b0a0e0a905aaa0f899704ac5b.htm

```


### Options
```
  -h, --help            show this help message and exit
  --dealer_url dealer_url
                        URL to the dealership homepage.
  --sort SORT           Sort the output table by a column
  --output {csv,json,table}
                        Format of the output, either csv, json, or table.
```