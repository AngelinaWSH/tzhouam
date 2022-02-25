import os
import csv
import pandas as pd
import atexit

#We define such a file system:
#    1: all files has such a structure: root -> index(a 8-bit string with number and characters) -> Year-> Month->file named by date

temp_files=[]  #a list that holds all temporary file

def exit_handler():#delete all temporary files
    for temp_file in temp_files:
        if(os.path.exists(temp_file)):
            os.remove(temp_file)
def delete_temp_files(root=os.path.abspath('.')+"\\"+"UQ"): #delete all temp files under the folder recursively
    files = os.listdir(root)
    for file in files:

        if (file[0:4] == "temp"):
            os.remove(root+"\\"+file)
        elif os.path.isdir(root+"\\"+file):
            delete_temp_files(root+"\\"+file)
        else:
            continue

def in_list(l,i):
    for f in l:
        if (f==i):
            return True
    return False

def open_all(root, save_path,save_name="temp.csv",index=""): #combine all files and store it in the input root

    if(os.path.isdir(root)):
        files=os.listdir(root)
        is_dir=True
    else:
        files=[root]
        is_dir=False

    global df
    if  not in_list(temp_files,save_path+"\\"+save_name): #add the created temp file into the list
        temp_files.append(save_path+"\\"+save_name)

    for file in files:
        if is_dir:
            path=root+"\\"+file
        else:
            path=root
        if os.path.isdir(path):
            open_all(path,save_path,save_name)
        elif (file[-4:]==".csv"):

            df = pd.read_csv(path)
            if(index==""):
                if not in_list(os.listdir(save_path),save_name):

                    df.to_csv(save_path + '\\' + save_name, encoding="utf_8_sig", index=False)#just the same as the previous csv file, no index

                else:

                    df.to_csv(save_path + '\\' + save_name, encoding="utf_8_sig", index=False, header=False, mode="a+")
            else:

                index_list=[]
                for _ in range(len(df)):
                    index_list.append(index)
                df.insert(0,"Index",index_list,True)

                if not in_list(os.listdir(save_path), save_name):

                    df.to_csv(save_path + '\\' + save_name, encoding="utf_8_sig",
                              index=False)  # just the same as the previous csv file, no index

                else:

                    df.to_csv(save_path + '\\' + save_name, encoding="utf_8_sig", index=False, header=False, mode="a+")

        else:
            continue


def open_index(index): #find all files of the index solar panel and combine them in a temp file then print the temp file in the terminal
    if(type(index).__name__=='int'):#change index from int to string
        index=str(index)
    root=os.path.abspath('.')
    path=root+"\\"+"UQ"
    files=os.listdir(root+"\\"+"UQ")
    for file in files:
        if( file == index):
            open_all(path+"\\"+index,path+"\\"+index)
            # with open(path+"\\"+index+"\\"+"temp.csv") as f:
            #     cr=csv.reader(f)
            #     for row in cr:
            #         print(row)
            return
    print("No such File")

def open_date(date):#date showed be in the follow format: yyyy-mm-dd or yyyy-mm or yyyy and it's a string
    root=os.path.abspath('.')+"\\"+"UQ"
    files=os.listdir(root)
    if (len(date)==10):
        year=date[:4]
        month=date[5:7]
        day=date[-2:]
    elif (len(date)==7):
        year=date[:4]
        month=date[5:]
        day="**"
    else:
        year=date[:4]
        month="**"
        day="**"

    for file in files:
        if(os.path.isdir(root+"\\"+file)):

            index_path=root+"\\"+file
            year_files=os.listdir(index_path)
            for year_file in year_files:

                if(year_file==year and os.path.isdir(index_path+"\\"+year_file)):

                    year_path=index_path+"\\"+year_file
                    month_files=os.listdir(year_path)
                    if(len(date)==4):
                        open_all(year_path,root,index=file)
                        continue
                    for month_file in month_files:
                        if (month_file==month and os.path.isdir(year_path+"\\"+month_file)):
                            month_path=year_path+"\\"+month_file
                            day_files=os.listdir(month_path)
                            if (len(date) == 7):
                                open_all(month_path, root,index=file)
                                continue
                            for day_file in day_files:
                                if (day_file[:2]==day and day_file[-4:]==".csv"):
                                    day_path=month_path+"\\"+day_file  #the path of the date file
                                    open_all(day_path,root,index=file)
                                    continue

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
    print("Start writing "+index+" at "+root+" with file at "+path)
    index=str(index)
    index_path=root+"\\"+index
    mkdir(index_path)
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        er=enumerate(reader)
        previous_day=''
        for rows in list(er):
            if (rows[0]==0):
                head=rows[1]
            else:
                #can be general used if all data conform the rule that date is at first and in the format of yyyy-mm-dd
                year=rows[1][0][0:4]
                month=rows[1][0][5:7]
                day = rows[1][0][8:10]
                mkdir(index_path+"\\"+year)
                mkdir(index_path+"\\"+year+"\\"+ month)
                with open(index_path+"\\"+year+"\\"+ month+"\\"+day+".csv",'a') as f:
                    writer=csv.writer(f)
                    if(day!=previous_day):
                        dict_writer=csv.DictWriter(f,fieldnames=head)
                        dict_writer.writeheader()
                    writer.writerow(rows[1])
                    previous_day=day
    print("Finished writing "+index)

def make_UQ():
    root = os.path.abspath('.')
    path=root+"\\2018WY"+"\\2018WY"
    files = os.listdir(path)
    mkdir(root+"\\"+"UQ")
    for f in files:
        index=f[20:]
        index=index[:-4:1]
        make_index(root+"\\"+"UQ",path+"\\"+f,index)
    print("Make UQ finished")
make_UQ()
# while True:
#     print("What do you want to do? (a: find by index, b: find by date, d:delete all temp files, e: exit)" )
#     c=input()
#     if (c=='a'):
#         print("Input the index")
#         i=input()
#         open_index(i)
#     elif (c=='b'):
#         print("Input date(yyyy-mm-dd/ yyyy-mm/ yyyy)")
#         d=input()
#         open_date(d)
#     elif (c=='d'):
#         delete_temp_files()
#         print("Temporary files deleted")
#     elif (c=='e'):
#         print('Exit!!!')
#         break
#     else:
#         print("Please enter a valid value.")
#         continue
# atexit.register(exit_handler)# delete all created tempfiles