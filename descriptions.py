import json
import csv

with open('R:\Python\Relaying Database\json\contract.json', 'r') as file:
        masterList = json.load(file)

with open('D:\Documents\Material.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    # material = dict(reader)
    # for i in reader:
    #     print(i)
    # material = dict((rows[0],rows[1]) for rows in reader)
    # print(reader.reader)
    keylist = []
    masterList = []
    for row in reader:
        keylist = row.keys()
        # print(row)
        masterList.append(row)
        # for column in row.keys():
keylist = list(keylist)        


output = []
# for i in range(len(masterList)):
#     print(type(masterList[i]))
#     output.append({masterList[i]['ItemNo'], masterList[i]})

output = []
itemlist = masterList[0]
itemnumber = itemlist['ItemNo']

output.append(itemnumber)
output.append(itemlist)

print(output)

out_file = open("masterlist.json", "w")
json.dump(output, out_file, indent=6)

# print(material)
def descriptions (item):
    '''item as dictionary list'''
    masterList[item]['description']