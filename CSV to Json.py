import json
import csv

file = open('material.csv', 'r')

adddiosdkjfnaoivjasd = file.readline().split(';')
itemKeys = file.readline().split(';')
firstItem = file.readline().split(';')

with open('./json/Basic Material.json', 'r') as file:
    basicItemDict = json.load(file)

itemDict = {}

print(len(itemKeys))
print(len(firstItem))

print(firstItem)
# for n,key in enumerate(itemKeys):
#     if firstItem[n] != '':
#         itemDict[key] = firstItem[n]

# print(itemDict)
# print(itemKeys)
# print(firstItem)
    