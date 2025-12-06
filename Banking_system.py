import json
import pandas as pd


def signup():
    print("------------------------------")
    name=input("Enter your name: ")

    with open("user_data.json","r") as f:
        aa=json.load(f)

        
        if name.lower() in aa:
            print("Id alredy exists")
            start()

        else:
            password=input("Enter a strong password: ")
            money=int(input("Enter amount: "))

            signup_data={
            name.lower():{
                "password":password,
                'money':money
                }
            }

            with open("user_data.json" , "r") as f:
                ha=json.load(f)
    
            ha.update(signup_data)

            with open("user_data.json","w") as f:
                json.dump(ha,f,indent=4)

            print("-------------------------------")
            print("login complete!!!!")
            print("-------------------------------")
             
            lagain=input("Want to login in? y/n: ")
            if lagain.lower()=="y":
                login()

            else:
                exit()

def login():

    sname=input("Enter your name: ")

    with open("user_data.json","r") as f:
        aa=json.load(f)
    
    if sname.lower()=="admin":
        admin()
        exit()

    else:

        spass=input("Enter your password:  ")

        with open("user_data.json","r") as f:
            ka=json.load(f)
            s1pass=ka[sname.lower()]["password"]
            mon1=ka[sname.lower()]["money"]

        if spass==s1pass:
            print("Welcome")
            print("Avaiable balance is: $ ",mon1)
        
        else:
            print("No user found")
            start()

def admin():
    apass=input("Enter the password:")
    if apass=="a":
        admin_control()

    else:
        print("You are not a admin")
        exit()


def admin_control():

    print("------------------------------")
    print("Welcome Admin")
    print("Admin control")
    print("------------------------------")

    print("1. See data ")
    print("2. Edit data")

    with open("user_data.json","r") as f:
            aa=json.load(f)
    
    data=pd.DataFrame.from_dict(aa,orient="index")
    data.reset_index(inplace=True)
    data.rename(columns={"index":"Coustmer names"} ,inplace=True)
    data.index +=1

    
    aa1=int(input("select [1][2]: "))
    print("-------------------------------")
    if aa1==1:
        print("User Info")
        print("-"*20)
        print(data)

    elif aa1==2:
        edit_data()

        again1=input("Want to change something else? y/n : ")
        if again1=="y":
            edit_data()
        
        elif again1=="n":
            # print("this works")
            a=input("Want to login again? y/n: ")
            if a=="y":
                login()

            else:
                exit()
        else:
            exit()

def edit_data():

    with open("user_data.json","r") as f:
            aa=json.load(f)
    
    data=pd.DataFrame.from_dict(aa,orient="index")
    data.reset_index(inplace=True)
    data.rename(columns={"index":"Coustmer names"} ,inplace=True)
    data.index +=1


    print(data)
    print("------------------------------")
    client=input("Enter the client name : ")
    data1=input("Enter the data you want to change password/money: ")

    if data1=="money":
        new_money=int(input("Enter the new balance: "))
        aa[client][data1]=new_money


    elif data1=="password":
        new_password=input("Enter the new password: ")
        aa[client][data1]=new_password

    with open("user_data.json","w") as f:
        json.dump(aa,f,indent=4)

    ndf=pd.DataFrame.from_dict(aa,orient="index")
    ndf.reset_index(inplace=True)
    ndf.rename(columns={"index":"coustmer names"},inplace=True)
    ndf.index +=1

    print(ndf)

        

def start():
    first=input("Are you an existing usser? y/n :")
    if first.lower() =="y" or first.lower()=="yes":
        print("------------------------------")
        print("Welcome")
        print("------------------------------")
        login()

    elif first.lower()=="n" or first.lower()=="no":
        print("------------------------------")
        print("you can sign up!!!!")
        signup()
    
    else:
        start()

start()