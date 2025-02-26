import json
import csv

with open("D:\Documents\Material.txt", mode='r') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    
    data_list = []
    
    for row in csv_reader:
        data_list.append(row)


       
for n in data_list:
    print(len(n))
    # if len(n) != 118:
    #     res = []
    #     res.append({k: v for k, v in n.items() if v})
    #     print(f"{n['ID']} - {len(n)} ({res})")

# adddiosdkjfnaoivjasd = file.readline().split(';')
# itemKeys = file.readline().split(';')
# firstItem = file.readline().split(';')

# with open('./json/Basic Material.json', 'r') as file:
#     basicItemDict = json.load(file)

# itemDict = {}



# print(len(itemKeys))
# print(len(firstItem))

# print(firstItem)
# for n,key in enumerate(itemKeys):
#     if firstItem[n] != '':
#         itemDict[key] = firstItem[n]

# print(itemDict)
# print(itemKeys)
# print(firstItem)
    