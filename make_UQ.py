import os
import csv
import pandas as pd
import atexit

def mkdir(path): #create a folder if the folder has already existed, skip it
    path=path.strip()
    path=path.rstrip()
    exist=os.path.exists(path)
    if not exist:
        os.mkdir(path)
        return True
    else:
        return False
def make_index(root,path,index):
    index=str(index)
    index_path=root+"\\"+index
    mkdir(index_path)
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        er=enumerate(reader)
        for rows in list(er):
            if (rows[0]==0):
                head=rows[1]
            else:
                year=rows[1][0][0:4]
                month=rows[1][0][5:7]
                day = rows[1][0][8:10]
                mkdir(index_path+"\\"+year)
                mkdir(index_path+"\\"+year+"\\"+ month)
                with open(index_path+"\\"+year+"\\"+ month+"\\"+day,'a') as f:
                    writer=csv.writer(f)
                    writer.writerow(rows[1])

def make_UQ():
    root = os.path.abspath('.')
    path=root+"\\2018WY"+"\\2018WY"
    files = os.listdir(path)
    mkdir(root+"\\"+"UQ")
    for f in files:
        index=f[20:]
        index=index[:-4:1]
        make_index(root+"\\"+"UQ",f,index)
make_UQ()