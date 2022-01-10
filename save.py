import os
from csv import writer
import openpyxl
import csv
FILE = os.path.join(os.getcwd(), "networkinfo.log")
csv_file=os.path.join(os.getcwd(), "networkinfo.csv")
excel_file=os.path.join(os.getcwd(), "networkinfo.xlsx")
template=["Date","Disconnected at","Connected at","Disconnected duration"]
with open(csv_file, 'w',newline="") as f_object:
  writer_object = writer(f_object)
  writer_object.writerow(template)
  f_object.close()

file = open(FILE, 'r')
lines = file.read().splitlines()
file.close()
get_index=[]
for index, line in enumerate(lines):
  if line=='':
    get_index.append(index)
new_list=[] 
for i in range(len(get_index)):
  if i!=len(get_index)-1:
    new_list.append(lines[get_index[i]:get_index[i+1]])
  else:
    new_list.append(lines[get_index[-1]:])


dict_writer={"Date":"",
              "Disconnected_at":"",
             "Connected_at":"",
             "Disconnected_duration":""}


j=0
for line in new_list:

  for i in line:
    
    if i=='CONNECTION ACQUIRED':
      pass
    if i.startswith("monitoring started at:"):
      st=i
      st=st.split("monitoring started at: ")
      data=st[-1].split(" ")
      date_format=data[0].replace(":","/")
      dict_writer["Date"]=date_format
    elif i.startswith("disconnected at:")==True:
      st=i
      st=st.split("disconnected at:")
      st=st[-1].split(" ")
      dict_writer["Disconnected_at"]=st[2]+" "+st[3]
      j=1
    elif i.startswith("connected again")==True:
      st=i
      st=st.split("connected again:")
      st=st[-1].split(" ")
      dict_writer["Connected_at"]=st[2]+" "+st[3]
      j=2
    
    elif i.startswith("connection was unavailable for:")==True:
      st=i
      st=st.split("connection was unavailable for: ")
      st=st[-1]
      dict_writer["Disconnected_duration"]=st
      j=3
    if j==3:
      create_list=list(dict_writer.values())
      with open(csv_file, 'a',newline="") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(create_list)
        f_object.close()
      j=0
  with open(csv_file, 'a',newline="") as f_object:
    writer_object = writer(f_object)
    writer_object.writerow("")
    f_object.close()

def csv_to_excel(csv_file, excel_file):
    csv_data = []
    with open(csv_file) as file_obj:
        reader = csv.reader(file_obj)
        for row in reader:
            csv_data.append(row)

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row in csv_data:
        sheet.append(row)
    workbook.save(excel_file)


if __name__ == "__main__":
    csv_to_excel(csv_file, excel_file)
