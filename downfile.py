import xlrd
import shutil
import os
import csv

filename = "downlist.csv"
f = open(filename, 'r')
rdr = csv.reader(f)
for line in rdr:
    fileName = line[0]
    # print(fileName)
    os.system('wget ' + fileName)