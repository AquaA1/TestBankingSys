import json
import pandas as pd
import hashlib
import getpass
import os

absolute_path=r"C:\Volume A\VS code codesss\gitt\TestBankingSys\user_data.json"

def user_name():
    username=input("Enter your nameeeeee: ")
    return username

name=None

def signup():
    global name
    if name is None:
        name=user_name()

    print("------------------------------")

    with open(absolute_path,"r") as f:
        aa=json.load(f)

        
        if name.lower() in aa:
            print("Id alredy exists")
            start()

        else:
            password=input("Enter a strong password: ")
            #hashing the password
            hashed_p=hashing_password(password)
            money=int(input("Enter amount to deposit: "))

            signup_data={
            name.lower():{
                "password":hashed_p,
                'money':money
                }
            }

            with open(absolute_path , "r") as f:
                ha=json.load(f)
    
            ha.update(signup_data)

            with open(absolute_path,"w") as f:
                json.dump(ha,f,indent=4)

            print("-------------------------------")
            print("login complete!!!!")
            print("-------------------------------")
             
            lagain=input("Want to login in? y/n: ")
            if lagain.lower()=="y":
                login()

            else:
                exit()

def hashing_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login():

    global sname
    sname=input("Enter your name: ")

    with open(absolute_path,"r") as f:
        aa=json.load(f)
    
    if sname.lower()=="admin":
        admin()
        exit()

    elif sname not in aa:
        print("No user found")
        ask_again=input("Want to try again? y/n:")
        if ask_again=="y":
            start()
        else:
            exit()

    else:

        spass=getpass.getpass("Enter your password:  ")
        spass_hashed=hashing_password(spass)

        with open(absolute_path,"r") as f:
            ka=json.load(f)
            s1pass=ka[sname.lower()]["password"]
            mon1=ka[sname.lower()]["money"]

        if spass_hashed==s1pass:
            print("Welcome")
            print("Avaiable balance is: $ ",mon1)
            user_control()
        
        else:
            print("Wrong password")
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

    with open(absolute_path,"r") as f:
            aa=json.load(f)
    
    data=pd.DataFrame.from_dict(aa,orient="index")
    data.reset_index(inplace=True)
    data.rename(columns={"index":"Coustmer names"} ,inplace=True)
    data.index +=1

    while True:
        try:
            aa1=int(input("select [1][2]: "))
        except:
            print("Choose correctly!!!")
            continue

        print("-------------------------------")
        if aa1==1:
            print("User Info")
            print("-"*20)
            print(data)
            aa11=input("Want to go back? y/n: ")
            if aa11=="y":
                continue
            else:
                exit()

        elif aa1==2:
            edit_data()

            again1=input("Want to change something else? y/n : ")
            if again1=="y":
                continue
            
            elif again1=="n":
                # print("this works")
                a=input("Want to login again? y/n: ")
                if a=="y":
                    login()

                else:
                    exit()
            else:
                exit()
        else:
            print("Choose correctly!!")
            continue



def edit_data():

    with open(absolute_path,"r") as f:
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

    with open(absolute_path,"w") as f:
        json.dump(aa,f,indent=4)

    ndf=pd.DataFrame.from_dict(aa,orient="index")
    ndf.reset_index(inplace=True)
    ndf.rename(columns={"index":"coustmer names"},inplace=True)
    ndf.index +=1

    print(ndf)

# def user_control():
#     with open(absolute_path,"r") as f:
#         temp=json.load(f)
#     user_depo=input("Want to see choices? y/n: ")
#     if user_depo=="y":
#         edit_data_u()
#     else:
#         exit()

def user_control():
    with open(absolute_path,"r") as f:
        aa=json.load(f)
        mon1=aa[sname.lower()]["money"]

    print("-"*20)
    print("[1]","\033[31m","Deposit money","\033[0m")
    print("[2]","\033[32m","Withdraw money","\033[0m")
    print("[3]  change Password")
    print("-"*20)    
    user_choice=int(input("What you want to do?:"))
    if user_choice==1:
        while True:
            try:
                depo_money=int(input("Enter the amout of money you want to deposit: "))
                aa[sname]["money"]=mon1+depo_money

                with open(absolute_path,"w") as k:
                    json.dump(aa,k,indent=4)
                print("Amount has been deposited")
                print("New balance is : $",aa[sname]["money"])

                break

            except ValueError:
                print("Enter money in numbers")
    
    elif user_choice==2:
        while True:
            try:
                withdraw_money=int(input("Enter the amout of money you want to withdraw: "))
                if aa[sname.lower()]["money"]<withdraw_money:
                    print("Not enough money") 
                else:
                    aa[sname.lower()]["money"]=mon1-withdraw_money

                    with open(absolute_path,"w") as k:
                        json.dump(aa,k,indent=4)

                    print("Money has been withdrawn")

                    print("Avalable balance: ","$", aa[sname.lower()]["money"])

                    break

            except ValueError:
                print("Enter money in numbers")

    elif user_choice==3:
        c_password=input("Enter your current password: ")

        with open(absolute_path, "r") as k:
            p=json.load(k)
            pcheck=p[sname.lower()]["password"]

            hash_c_password=hashing_password(c_password)

        if hash_c_password==pcheck:
            c_password=input("Enter new password: ")
            hash_c_password=hashing_password(c_password)
            
            p[sname]["password"]=hash_c_password

            with open(absolute_path,"w") as k:
                json.dump(p,k,indent=4)
            print("Password succesfully changed!!!!")
            print("-"*20)
            print("Your are logged out login again")
            login()



    else:
        print("Re-enter")
            

        

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