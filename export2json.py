import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from collections import namedtuple

import pprint
pp = pprint.PrettyPrinter(indent=4)

tree = ET.parse('./Export_2017_04_13-14_12.xml')
root = tree.getroot()

# build catalog of products
products = {}
for product in root.iter('product'):
    product_id = int(product.get('id'))
    name = product.get('desc1_default')
    if not "TEST" in name:
        # skip those products
        products[product_id] = name
pp.pprint(products)

# data for the punchcard plot
Punch = namedtuple("Punch", ["day_of_week", "time_of_day"])
punchcard_data = {}

# product ranking
product_ranking = {}

# products by time of day
product_times = {}

# we know that the machine did not adjust the date correctly -
# the 29th of february was skipped. The date was then adjusted at some point.
# Because the data is ordered by date we can adjust this issue:
# Each date after the 29th is sent back in time until we parse a new date that
# is before the last parsed date.
last_entry_date_time = datetime(1970, 1, 1)
adjust_date_time = True

# count the number of days included in export
total_workdays = 0

# all productions
total_productions = 0

for entry in root.iter('hires_consumption_entry'):

    # sample:
    # <hires_consumption_entry 
    #   id="1"
    #   date="08_02_2016_10_46_05_000"
    #   coffee_amount_set="12"
    #   coffee_amount_used="10.1176"
    #   brew_duration="4"
    #   grinder="1"
    #   days="2"
    # />

    # fix time issue -----
    # february 29th was skipped, the date was later fixed manually
    entry_date_time = datetime.strptime(entry.get('date'), '%d_%m_%Y_%H_%M_%S_%f')
    if entry_date_time < last_entry_date_time:
        # time was adjusted manually
        adjust_date_time = False

    if entry_date_time > datetime(2016, 2, 29) and adjust_date_time:
        correct_date_time = entry_date_time - timedelta(days=1)
    else:
        correct_date_time = entry_date_time
    # end fix ------------

    # workday counter
    if last_entry_date_time.date().day != entry_date_time.date().day:
        total_workdays += 1
    last_entry_date_time = entry_date_time

    # production counter
    total_productions += 1
    
    product_id = int(entry.get('id'))
    
    # manipulate ids > 10000 (app products) to their base product
    if product_id > 10000
    product_id = product_id / 10
    
    # skip products that are not in catalog
    if not product_id in products:
        continue

    # create ranking (products with different ids but the same  
    # name will be be treated as the same product).
    if not products[product_id] in product_ranking:
        product_ranking[products[product_id]] = 0
    product_ranking[products[product_id]] += 1


    # gather data for punchcard plot
    punch = Punch(day_of_week=(correct_date_time.weekday() + 1) % 6, time_of_day=correct_date_time.hour)
    if not punch in punchcard_data:
        punchcard_data[punch] = 0
    punchcard_data[punch] += 1
    # -----

    # gather data for bar chart
    # we use the most frequently requested products (ranking done manually)
    name = products[product_id]
    if (u'\xa0Caf\xe9 Cr\xe8me' in name or
            'Tee' in name or
            'Cappuccino' in name or
            u'Latte\xa0Macchiato' in name):
        if u'\xa0Caf\xe9 Cr\xe8me' in name:
            # combine Cafe Creme and Cafe Creme Pott
            name = u'\xa0Caf\xe9 Cr\xe8me'
        if 'Cappuccino' in name:
            name = 'Cappuccino'

        if not name in product_times:
            product_times[name] = [0]*15

        product_times[name][correct_date_time.hour -6] += 1



# print punchcard data to array for integration in punchcard.html
#for item in punchcard_data:
#    print('[' + str(item.day_of_week) + ',' + str(item.time_of_day) + ',' + str(punchcard_data[item]) + '],')
### -----

# print products by time data for integration in barchart.html
#print('Product, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18')
#for item in product_times:    
#    print(item + ',' + str(product_times[item]))
### -----


#pp.pprint(product_ranking)
#pp.pprint(punchcard_data)
#pp.pprint(product_times)
