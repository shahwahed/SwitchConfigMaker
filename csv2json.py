#!/usr/bin/python
#quick & dirty csv to json with python

from collections import OrderedDict
import csv
import json

#csv_file = 'vlan.csv'
csv_file = 'csv/mapping_port_sw01.csv'
json_file = 'json/mapping_port_sw01.json'


#Open csv

with open(csv_file,'rU') as f_csv:
    reader = csv.reader(f_csv)
    headerlist = next(reader)
    csvlist = []
    for row in reader:
        data = OrderedDict()
        for i, x in enumerate(row):
            data[headerlist[i]] = x
        csvlist.append(data)
    json_out = json.dumps(csvlist, indent=4)
    f_csv.close()

#save json
with open(json_file,'w') as f_json:
    f_json.write(json_out)
    f_json.close()
