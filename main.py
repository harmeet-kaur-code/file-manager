from pathlib import Path
import os

def createfile():
    try:
        name=input("enter the file name:-")
        path=Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data=input("what you want to write:")
                fs.write(data)
            print("File created successfully")
        else:
            print("ERROR File name is already exists")
    except Exception as err:
        print(f"an error occured as {err}")    
def readfile():
    try:
        name=input("Enter the file name:-")
        path=Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content=fs.read()
                print(f"Your file content is \n {content}")
        else:
            print("ERROR No such file exists")
    except Exception as err:
        print(f"An error occured as {err}")

def updatefile():
    try:
        name=input("Enter the file name:-")
        path=Path(name)
        if path.exists:
            print("Operations")
            print("1. Renaming the file")
            print("2. Appending the file")
            print("3.Overwriting the file")
            choice=int(input("Enter your option:-"))
            if choice==1:
                newname=input("Enter your new file name:-")
                new_path=Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("Renamed Successfully")
                else:
                    print("File already exists") 
            elif choice==2:
                with open(path,'a') as fs:
                    data=input("what do you want to appened:-")  
                    fs.write(" \n"+data)
                print("Successfully Appended")
            elif choice==3:
                with open(path,"w") as fs:
                    data=input("what do you want to overwrite:-")  
                    fs.write(" \n"+data)
                print("Successfully Overwrittened")
    except Exception as err:
        print(f"An error occoured as {err}")
def deletefile():
    try:
        name=input("Enter the file name:")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("File deleted successfully")
        else:
            print("ERROR no such file exists")
    except Exception as err:
        print(f"An error occoured as {err}")

print("Press 1 for creating a file")
print("Press 2 for reading a file")
print("Press 3 for updating a file")
print("Press 4 for  deleting a file")
a=int(input("\n Tell your response:-"))
if a==1:
    createfile()
if a==2:
    readfile()
if a==3:
    updatefile()
if a==4:
    deletefile()

