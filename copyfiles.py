import xlrd
import shutil
import os
import csv

filename = "/data/test_sample.csv"
f = open(filename, 'r')
rdr = csv.reader(f)
for line in rdr:
    fileName = line[1]
    print(fileName)
    shutil.copy("/root/kisa/train_set/"+fileName , "/data/myAI/dataset/trainset/")
