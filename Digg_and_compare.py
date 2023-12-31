import tkinter as tk
from tkinter import IntVar
#from tkinter import * to specify what to import from tkinter
from simple_salesforce import Salesforce
from tkinter.scrolledtext import ScrolledText #used to display the Long Text Area input field for the SOQL query
from tkinter import messagebox #To display error or success message
import requests #to handle exception in request to SF
import csv #needed to create CSV file
import pprint #to show the result of data extracted with Salesforce Query
from collections import OrderedDict #object retrieved via Query needed to iterate in order to obtain all values extracted
# import filedialog module
from tkinter import filedialog
from simple_salesforce.exceptions import *
#import pandas as pd
import os #needed for resource_path func
import sys #needed for resource_path func

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#This function resource_path is needed if we have some assets (images, fonts, etc..) in local folders. Pyinstaller is expecting to find your assets as images, data and fonts inside a temporary folder instead named sys._MEIPASS, which is very different from the project folder which is not temporary. This function helps pyinstaller finding the correct location of our assets. For each point where we should load local resources, we have to use this function (ex ---> "assets/logo.png" becomes resource_path("assets/logo.png"))
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



master = tk.Tk()
sf = "test"
enable_query = False

#to set the window with commands
master.geometry("800x600")
master.title("Data Digger")
#label = tk.Label( master, text="Dig your data!", font=('Arial',18) )

#Input credentials
tk.Label(master, text="UserName").grid(row=0)
tk.Label(master, text="Password").grid(row=1)
tk.Label(master, text="Security Token").grid(row=2)
tk.Label(master, text="Domain").grid(row=3)


inputName = tk.Entry(master,width=50, font=('Helvetica 10'))
orgPassword = tk.Entry(master,width=50, font=('Helvetica 10'))
securityToken = tk.Entry(master,width=50, font=('Helvetica 10'))
orgDomain = tk.Entry(master,width=50, font=('Helvetica 10'))

inputName.grid(row=0, column=1, sticky=tk.W)
orgPassword.grid(row=1, column=1, sticky=tk.W)
securityToken.grid(row=2, column=1, sticky=tk.W)
orgDomain.grid(row=3, column=1, sticky=tk.W) #Sticky specifies a value of S = South, N=North, E=East, W=West, to make the value of the cell be aligned  to the margin Left (West), Right(East), Up (North), Down(South) or a combination of them. In this case we uase sicky = W because we want it to be aligned to the margin left of the column cell



#outputFilePath.grid(row=8, column=1)

#csvFromQueryPath = tk.StringVar() #StringVar() is used to store String variables outside methods


#this section is just to put predefined values to test the functionality
#this section is just to put predefined values to test the functionality


#Test connection button
def show_entry_fields():
    try:
        userName = inputName.get()
        pwd = orgPassword.get()
        token = securityToken.get()
        domainName = orgDomain.get()
        
        print("Username: %s\norgPassword: %s\nSecurity Token: %s\n Domain: %s" % (userName, pwd,token,domainName))

        sf = Salesforce(username=userName, password=pwd, security_token=token,domain=domainName)
        print("sf ******")
        print(sf)
        sessionId = sf.session_id
        if (sessionId) :
            queryButton.config(state=tk.NORMAL)
            tk.messagebox.showinfo(title=None, message="Connection Successfull")
    except Exception as ex:
        print("ERROR During connection")
        queryButton.config(state=tk.DISABLED)
        tk.messagebox.showerror(title="ERROR During connection", message={ex})
  # except :
  #     print("Invalid login")
  #     tk.messagebox.showerror(title=None, message="Invalid login credentials")
  #     queryButton.config(state=tk.DISABLED)

testConnectionButton = tk.Button(master, 
                                text='Test Connection', 
                                command=show_entry_fields)

testConnectionButton.grid(row=4, column=0, sticky=tk.W,padx=(10, 0),pady=(10, 20))

#Query box section
#tk.Label(master, text="").grid(row=5)
queryBox = ScrolledText(master, width=90, height=10,font=('Helvetica 10'))
queryBox.grid(row=5, column=1, sticky=tk.W)

#Run query buttons
def run_query():
    print("csvFromQueryPath ****> " + csvFromQueryPath.get())
    if(csvFromQueryPath.get() == ''):
        print("inside if error query path ")
        tk.messagebox.showerror(title="No selected path", message="Please select path to save query result")
        return
    print("queryBox ****> " % queryBox)
    print("queryBox.get ****> " + queryBox.get('1.0', tk.END) )
    query = queryBox.get('1.0', tk.END) #Here 1.0 means start getting text from first character of the first line and end-1c means select text till the end and -1c means removing 1 character from the end as a newline \n character is added at the end of the text
    try:
        userName = inputName.get()
        pwd = orgPassword.get()
        token = securityToken.get()
        domainName = orgDomain.get()
        sf = Salesforce(username=userName, password=pwd, security_token=token,domain=domainName)
        print("sf ******")
        print(sf)
        data = sf.query_all(query)
        #pprint.pprint(data, sort_dicts=False)
        csv_data = []  # Initialize a list to hold CSV rows
        headerRow = []
        for header in data['records'][0].keys():
            print("header ****** " + header)
            if (header != "attributes"):   #this part here is to remove "attributes" value that is unnecessary and is built like this ('attributes', OrderedDict([('type', 'Contact'),('url','services/data/v57.0/sobjects/Contact/0039E00001nRXMwQAO')])),
                headerRow.append(header)

        csv_data.append(','.join(headerRow))  # Add CSV header removing "attributes" value 

        for record in data['records']:
            rowDetail = []
            for field, value in record.items(): #field is Key of map, value is the Value related to that key. Map is like this --> ('Name', 'TestName')
                if(field == "attributes"):
                    #rowDetail.append('test')
                    continue
                else:
                    if(value):
                        rowDetail.append(value)
                    else:
                        rowDetail.append('')
            csv_data.append(','.join(rowDetail))
        with open(csvFromQueryPath.get(), 'w') as file: # w = write, wb = write binary mode , b = binary
            file.write('\n'.join(csv_data))
        tk.messagebox.showinfo(title="Success", message="Query successfully completed")
  #  except SalesforceMalformedRequest as e:
  #      print("Invalid Query")
  #      tk.messagebox.showerror(title="Malformed Query", message={e})
    except Exception as ex :
        tk.messagebox.showerror(title="Query Error", message={ex})

queryButton = tk.Button(master, 
            text='Run Query',
            state="normal", 
            command=run_query,)

queryButton.grid(row=5, column=0, sticky=tk.W, pady=4,padx=(10, 0))

#method to open file browser and select file already existing
def loadCsv():
    filePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a Csv File",
                                          filetypes = (("Csv files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
    return filePath

#method to open file browser and create new file
def createCsv():
    filePath = filedialog.asksaveasfilename(confirmoverwrite=True,
                                            filetypes=[("csv file", ".csv")],
                                            defaultextension=".csv")
    return filePath

# Create a File Explorer Entry
csvFromQueryPath = tk.Entry(master,width=100 )
csvFromQueryPath.grid(row = 8, column = 1, sticky=tk.W)

# file explorer window
def browseFolders():
    csvFromQueryPath.delete(0, tk.END)
    print("csvFromQueryPath after RESET ****** " + csvFromQueryPath.get())
    filePath = createCsv() 
    csvFromQueryPath.insert(0,filePath)


#tk.Label(master, text="Output File Path").grid(row=8,pady=(10, 0))

button_explore = tk.Button(master,
                            text = "Select Folder to Save Query",
                            command = browseFolders)

button_explore.grid(row=8, column=0, sticky=tk.W, padx=(10, 0),pady=(10, 0))


#Load file CSV section
csvFromExternalPath = tk.Entry(master,width=100 )
csvFromExternalPath.grid(row = 11, column = 1, sticky=tk.W)

#tk.Label(master, text="File to Upload").grid(row=11,pady=(10, 0))


def updateExternalPath():
    csvFromExternalPath.delete(0, tk.END)
    print("csvFromExternalPath after RESET ****** " + csvFromExternalPath.get())
    filePath = loadCsv() 
    csvFromExternalPath.insert(0,filePath)

def updateLocalFilePath():
    csvFromLocalUser.delete(0, tk.END)
    print("csvFromLocalUser after RESET ****** " + csvFromLocalUser.get())
    filePath = loadCsv() 
    csvFromLocalUser.insert(0,filePath)

def chooseFileDirectory():
    fileDirectoryPath.delete(0, tk.END)
    print("fileDirectoryPath after RESET ****** " + fileDirectoryPath.get())
    filePath = createCsv()
    if(filePath != ""):
        fileDirectoryPath.insert(0,filePath)

loadFileButton = tk.Button(master,
                        text = "Upload External Csv",
                        command = updateExternalPath)

loadFileButton.grid(row=11, column=0, sticky=tk.W, padx=(10, 0),pady=(10, 0))

#Load query already done section
csvFromLocalUser = tk.Entry(master,width=100 )
csvFromLocalUser.grid(row = 12, column = 1, sticky=tk.W)

#Manual add already existing file from generated Query
uploadAlreadyExistingCsv = tk.Button(master,
                        text = "Upload already existing file",
                        command = updateLocalFilePath)

uploadAlreadyExistingCsv.grid(row=12, column=0, sticky=tk.W, padx=(10, 0),pady=(10, 0))

#Choose file directory where to save file from Compare
fileDirectoryPath = tk.Entry(master,width=100 )
fileDirectoryPath.grid(row = 16, column = 1, sticky=tk.W)

chooseFileDirectoryButton = tk.Button(master,
                            text = "Select folder to save Compare result",
                            command = chooseFileDirectory)

chooseFileDirectoryButton.grid(row=16, column=0, pady=(20, 0))


#Compare two CSV files section
def compareFiles():
    print("\n csvFromExternalPath ****>  ")
    print(csvFromExternalPath.get())
    print("\n csvFromQueryPath ****>  ")
    print(csvFromQueryPath.get())
    print("\n csvFromLocalUser ****>  ")
    print(csvFromLocalUser.get())
    
    queryPath = ''

    if(fileDirectoryPath.get() == ''):
        tk.messagebox.showerror(title="No selected path", message="Please select path to save compare result")
        return

    if(csvFromQueryPath.get() != ""):
        queryPath = csvFromQueryPath.get()
    else:
        queryPath = csvFromLocalUser.get() 

    print("queryPath ****> \n ")
    print(queryPath)
    
    try:
    #   with open(csvFromExternalPath.get(), 'r') as t1, open(queryPath, 'r') as t2:
    #       extCsv = t1.read().splitlines() #this splitlines() method splits removing all /n, /r, etc... https://www.geeksforgeeks.org/python-string-splitlines-method/
    #       csvQuery = t2.read().splitlines() #this splitlines() method splits removing all /n, /r, etc... https://www.geeksforgeeks.org/python-string-splitlines-method/

        with open(csvFromExternalPath.get(), 'r') as t1, open(queryPath, 'r') as t2:
            extCsv = set(t1)  #make a set out of the first file (fast lookup, and saves memory if there are duplicate lines) https://stackoverflow.com/questions/50107166/faster-way-to-compute-difference-between-two-csv-files
            csvQuery = set(t2)  #make a set out of the first file (fast lookup, and saves memory if there are duplicate lines) https://stackoverflow.com/questions/50107166/faster-way-to-compute-difference-between-two-csv-files

        #print("EXTcsv ****> \n ")
        #print(extCsv)
        #print("csvQuery ****> \n ")
        #print(csvQuery)
        #print('fileDirectoryPath.get() ************** ')
        #print(fileDirectoryPath.get())
        with open(fileDirectoryPath.get(), 'w') as outFile:
            outFile.write(("****** CHECK FROM FILE1 to FILE2 ******* \n\n"))
            count = 0
            for line in extCsv:
               # print("line extCsv ****> ")
               # print(line)
                #writing the first row every time because it's the header
                #if(count == 0):
                #    print("printing first line  ****> ")
                #    print(line)
                #    outFile.write(line+("\n")) #we have to write the first row because it's the header, even if there are no differencies
                if line not in csvQuery:
                    #outFile.write(line+("\n"))
                    outFile.write(line)
                count=count+1

            outFile.write(("\n\n ****** CHECK FROM FILE2 to FILE1 ******* \n\n"))

            for line in csvQuery:
               #print("line csvQuery ****> ")
               #print(line)
                if line not in extCsv:
                    #outFile.write(line+("\n"))
                    outFile.write(line)
                    
        tk.messagebox.showinfo(title="Success", message="Compare operation successfully completed")

    except Exception as ex :
        tk.messagebox.showerror(title="Compare file error", message={ex})
    
#compareFilesButton = tk.Button(master,
#                        text = "Compare Csv",
#                        command = compareFiles)
#
#compareFilesButton.grid(row=17, column=1, pady=(20, 0))

#Compare files button
compareFilesButton = tk.Button(master,
                        text = "Compare Files",
                        command = compareFiles)

compareFilesButton.grid(row=17, column=1)


master.mainloop()