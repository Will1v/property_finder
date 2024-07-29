
# Property finder

This tool will help you query the website OnTheMarket.com to find UK properties for sale, with certain criteria, and will give you a bit of insight on pricing.

## Authors

* William Vizard
    - GitHub: [@Will1v](https://github.com/Will1v)
    - EdX: [Will1v](https://cs50.me/cs50p)
    - London, United Kingdom
    - Demo video (recorded on 27/03/2024): [Youtube](https://youtu.be/8_-5XLfIbCs)

## Installation

This requires Python3 and the libraries specified in requirements.txt, which you can install with:

```
  pip install -r requirements. txt
```

## Documentation

Usage:

```
    usage: project.py [-h] --postcode POSTCODE --radius RADIUS [--min-price MIN_PRICE] [--max-price MAX_PRICE] [--min-bed MIN_BED] [--max-bed MAX_BED] [--type {house,flat}] [--potential] [--keywords KEYWORDS] [--debug]
project.py: error: the following arguments are required: --postcode, --radius
```

Where:

- Required fields:
    * postcode: postcode of the search you want to run. Eg: "SW1A 1AA"
    * radius: how far from the postcode you want to look, in miles (minimum will always be 0.25 miles)
- Optional fiels:
    * min/max-price: price bracket for the search, in British Pounds
    * mix/max-bed: minimum and/or maximum of bedrooms
    * type: type of property (house, flat...)
    * potential: use this flag if you only want properties that have potential to extend or need to refurb work
    * keywords: keywords you want to see (eg: garden, parking, spacious...). The search will return any property that has at least one of these keywords


## Usage/Examples

Searching 2/3 bedroom properties within 0.5 miles of Buckimgham Palace in a price range or £700k-2,000k, which have at least one of these criteria: a garden, some parking, a fireplace or a mantelpiece:

```
project/ $ python project.py --postcode "SW1A 1AA" --radius .5 --min-bed 2 --max-bed 3 --min-price 700000 --max-price 2000000 --keywords garden,parking,fireplace,mantelpiece
2024-03-27 14:14:31,898 [project.py:20][INFO] Results:
Results
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| Postcode |   Price    |  £/m2   | Benchmark | Stamp duty | Beds | Surface |   Type    |      Days since       |             Desc             |                      URL                       | Potential |  Keywords found   |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0NY |  £825,000  |    -    |     -     |  £20,000   |  2   |    -    |   Flat    |   Reduced yesterday   |   2 bedroom flat for sale    | https://www.onthemarket.com//details/13042679/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0NY | £1,100,000 |    -    |     -     |  £33,750   |  2   |    -    |   Flat    | OnTheMarket > 14 days |   2 bedroom flat for sale    | https://www.onthemarket.com//details/13904342/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1V 1AF | £1,175,000 |    -    |     -     |  £37,500   |  2   |    -    |   Flat    | OnTheMarket > 14 days |   2 bedroom flat for sale    | https://www.onthemarket.com//details/14304538/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1H 0HZ | £1,750,000 |    -    |     -     |  £66,250   |  2   |    -    |   Flat    | OnTheMarket > 14 days |   2 bedroom flat for sale    | https://www.onthemarket.com//details/14185548/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1H 0HX | £1,500,000 |    -    |     -     |  £53,750   |  2   |    -    |   Flat    | OnTheMarket > 14 days |   2 bedroom flat for sale    | https://www.onthemarket.com//details/13924588/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1V 1AA |  £900,000  | £9,375  |   -32%    |  £23,750   |  3   |  96 m2  | Apartment | OnTheMarket > 14 days | 3 bedroom apartment for sale | https://www.onthemarket.com//details/13711382/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1P 2QB | £1,000,000 | £10,000 |   -28%    |  £28,750   |  2   | 100 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/13753949/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0PR | £1,250,000 | £11,792 |   -15%    |  £41,250   |  2   | 106 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/13362946/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1H 9NJ | £1,195,000 | £12,070 |   -13%    |  £38,500   |  2   |  99 m2  |  Duplex   | OnTheMarket > 14 days |  2 bedroom duplex for sale   | https://www.onthemarket.com//details/14021400/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1H 0HU | £1,075,000 | £12,215 |   -12%    |  £32,500   |  2   |  88 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/12599503/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1P 1HN | £1,450,000 | £12,831 |    -8%    |  £51,250   |  2   | 113 m2  |   Flat    | OnTheMarket > 14 days |   2 bedroom flat for sale    | https://www.onthemarket.com//details/12816436/ |     -     | garden, fireplace |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1P 1HW | £1,500,000 | £13,043 |    -6%    |  £53,750   |  3   | 115 m2  |   Flat    | OnTheMarket > 14 days |   3 bedroom flat for sale    | https://www.onthemarket.com//details/14423725/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1P 1HW | £1,500,000 | £13,043 |    -6%    |  £53,750   |  3   | 115 m2  | Apartment | OnTheMarket > 14 days | 3 bedroom apartment for sale | https://www.onthemarket.com//details/14423481/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1P 1HN | £1,500,000 | £14,018 |    0%     |  £53,750   |  2   | 107 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/12039719/ |     -     |      garden       |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0PB | £1,700,000 | £17,171 |    22%    |  £63,750   |  2   |  99 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/13210376/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| SW1E 6AL | £1,800,000 | £19,354 |    38%    |  £68,750   |  2   |  93 m2  | Apartment | OnTheMarket > 14 days | 2 bedroom apartment for sale | https://www.onthemarket.com//details/13374953/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
| W1J 8AE  | £1,500,000 | £22,727 |    62%    |  £53,750   |  2   |  66 m2  |   Flat    |   Reduced yesterday   |   2 bedroom flat for sale    | https://www.onthemarket.com//details/13291660/ |     -     |      parking      |
+----------+------------+---------+-----------+------------+------+---------+-----------+-----------------------+------------------------------+------------------------------------------------+-----------+-------------------+
17 results found - Average £/m2: 13,969

Area stats (0.5 miles around SW1A-1AA):
+---------------+--------------+---------------------------+
| Property type | Average £/m2 | # of properties in sample |
+---------------+--------------+---------------------------+
|     Flat      |   £13,969    |            12             |
+---------------+--------------+---------------------------+
|    Garage     |      £0      |             0             |
+---------------+--------------+---------------------------+
|     House     |      £0      |             0             |
+---------------+--------------+---------------------------+
|     Other     |      £0      |             0             |
+---------------+--------------+---------------------------+
|      All      |   £13,969    |            12             |
+---------------+--------------+---------------------------+
```

### Known errors/edge cases

* Crazy price per square metre *

Some listings have incorrect surface which leads to absurd price per sqm which would lead to distorted averages. These are excluded. For example:

```
project/ $ python project.py --postcode "SW1A 1AA" --radius .5 --min-bed 2 --max-bed 3 --keywords garden,parking,fireplace,mantelpiece
[...]
2024-03-27 14:11:20,024 [project.py:36][ERROR] Skipping property https://www.onthemarket.com//details/14191724/ which has a crazy price per sqm (most likely due to incorrect surface)
2024-03-27 14:11:20,024 [project.py:36][ERROR] Skipping property https://www.onthemarket.com//details/13951425/ which has a crazy price per sqm (most likely due to incorrect surface)
2024-03-27 14:11:20,064 [project.py:20][INFO] Results:
Results
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+
| Postcode |    Price    |  £/m2   | Benchmark | Stamp duty | Beds | Surface |      Type      |      Days since       |               Desc                |                      URL                       | Potential |  Keywords found   |
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0NY |  £825,000   |    -    |     -     |  £20,000   |  2   |    -    |      Flat      |   Reduced yesterday   |      2 bedroom flat for sale      | https://www.onthemarket.com//details/13042679/ |     -     |      parking      |
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 9DB | £9,999,000  |    -    |     -     |  £478,700  |  3   |    -    |   Penthouse    |   Reduced < 7 days    |   3 bedroom penthouse for sale    | https://www.onthemarket.com//details/13310836/ |     -     |      garden       |
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+
| SW1W 0NY | £1,100,000  |    -    |     -     |  £33,750   |  2   |    -    |      Flat      | OnTheMarket > 14 days |      2 bedroom flat for sale      | https://www.onthemarket.com//details/13904342/ |     -     |      parking      |
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+
| ...
+----------+-------------+---------+-----------+------------+------+---------+----------------+-----------------------+-----------------------------------+------------------------------------------------+-----------+-------------------+

49 results found - Average £/m2: 22,209

Area stats (0.5 miles around SW1A-1AA):
+---------------+--------------+---------------------------+
| Property type | Average £/m2 | # of properties in sample |
+---------------+--------------+---------------------------+
|     Flat      |   £20,592    |            21             |
+---------------+--------------+---------------------------+
|    Garage     |      £0      |             0             |
+---------------+--------------+---------------------------+
|     House     |   £23,983    |             4             |
+---------------+--------------+---------------------------+
|     Other     |   £31,160    |             3             |
+---------------+--------------+---------------------------+
|      All      |   £22,209    |            28             |
+---------------+--------------+---------------------------+
```

* Property type not known warning *

Some listings have a property type that's too generic, such as "Property", or "Mews" (which could be flats or houses) and therefore cannot be classified as a house or a flat.
The warning is there to highlight types that might need to be added to the `OnTheMarketSearch.detailed_to_general_property_type_map` map but are generally safe to ignore.

eg:

```
project/ $ python project.py --postcode "SW1A 1AA" --radius .5 --min-bed 2 --max-bed 3 --keywords garden,parking,fireplace,mantelpiece
2024-03-27 14:10:46,634 [otm_helper.py:193][WARNING] Property type not known: Property (https://www.onthemarket.com//details/14267028/)
2024-03-27 14:10:53,533 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/13956588/)
2024-03-27 14:10:55,928 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/13929910/)
2024-03-27 14:10:57,879 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/13910535/)
2024-03-27 14:10:58,568 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/13896101/)
2024-03-27 14:10:58,956 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/13874672/)
2024-03-27 14:11:16,378 [otm_helper.py:193][WARNING] Property type not known: Property (https://www.onthemarket.com//details/12328823/)
2024-03-27 14:11:19,599 [otm_helper.py:193][WARNING] Property type not known: Mews (https://www.onthemarket.com//details/7669973/)
2024-03-27 14:11:20,024 [project.py:36][ERROR] Skipping property https://www.onthemarket.com//details/14191724/ which has a crazy price per sqm (most likely due to incorrect surface)
2024-03-27 14:11:20,024 [project.py:36][ERROR] Skipping property https://www.onthemarket.com//details/13951425/ which has a crazy price per sqm (most likely due to incorrect surface)
2024-03-27 14:11:20,064 [project.py:20][INFO] Results:
[...]
```
