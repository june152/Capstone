import os
import sys
from subprocess import Popen
import subprocess

path = sys.argv[1]
print (path)
temp = os.getcwd()
batfile = "upxunpacker.bat"
batfilepath = os.path.join(temp,batfile)
print (batfilepath)

for root,dirs,files in os.walk(path,topdown=False):
    for upxfile in files:
        upxfilename = os.path.join(path,upxfile)
        print (upxfilename)
        f = open(batfilepath,'w')
        f.close()
        with open (batfilepath,'a+') as writefile :
            writefile.write("/root"+"\n") #Change Dir Loc if you pasted in other Directory
            writefile.write("cd /root/upxunpacker"+"\n") #Change Folder loc if you pasted in other locations
            writefile.write("upx.exe -d "'"'+upxfilename+'"'"\n")
            writefile.write("Exit")
        subprocess.call(batfilepath,stdin=None,stdout=None,stderr=None,shell=False)