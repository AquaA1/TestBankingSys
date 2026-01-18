import json
import pandas as pd
import hashlib
import getpass
#import os
from datetime import datetime

now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
absolute_path=r"C:\Volume A\VS code codesss\gitt\TestBankingSys\user_data.json"
control_j=r"C:\Volume A\VS code codesss\gitt\TestBankingSys\control.json"
admin_notification=r"C:\Volume A\VS code codesss\gitt\TestBankingSys\admin_notification.json"

def save_data_user(data):
    with open(absolute_path, "w") as f:
        json.dump(data,f,indent=4)

def read_data_user():
    with open(absolute_path, "r") as f:
        return json.load(f)
    
def save_data_admin_notifi(data1):
    with open(admin_notification,"w") as f:
        json.dump(data1,f,indent=4)

def read_data_admin_notifi():
    with open(admin_notification,"r") as f:
        return json.load(f)
    
def read_data_control():
    with open(control_j,"r") as f:
        return json.load(f)
    


def signup():
    global name
    name=input("Enter your name: ")

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
            
            while True:
                input_date=input("Enter your date of birth: YYYY-MM-DD format only: ")
                try:
                    dob=datetime.strptime(input_date, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("invalid date")

            signup_data={
            name.lower():{
                "password":hashed_p,
                "password_type":"custom",
                'money':money,
                "DOB":dob.isoformat(),
                "admin_ctrl":False
                }
            }

            with open(absolute_path , "r") as f:
                ha=json.load(f)
    
            ha.update(signup_data)

            with open(absolute_path,"w") as f:
                json.dump(ha,f,indent=4)

            his_transfer={
                "type":"First depo",
                "from": "self",
                "to": "self",
                "amount":money,
                "date and time":now
            }

            his_create={
                name.lower():{
                    "history":[

                    ]
                }
            }

            with open(control_j , "r") as k:
                ma=json.load(k)
            
            ma.update(his_create)
            #ma[name]["history"].append(create_time)
            ma[name]["history"].append(his_transfer)

            with open(control_j, "w") as m:
                json.dump(ma,m,indent=4)

# addinng initial data to admin_notification

            load_admin_notifi=read_data_admin_notifi()
            
            load_admin_notifi.update({
                name :{
                    "notif": "nill"
                }
            })
            save_data_admin_notifi(load_admin_notifi)


            

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
    while True:
        sname=input("Enter your name: ")

        change_p_notif=read_data_user()

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
            if change_p_notif[sname]["password_type"]=="default":
                print("Password has been set to defaut by ADMIN")
                print("Your password is your dob in YYYY-MM-DD format")

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
                break
            
            else:
                print("Wrong password")
                print("[1] Try again")
                print("[2] Forget password")
                f_pass=int(input("Enter your choice: "))
                if f_pass==1:
                    continue
                
                elif f_pass==2:
                    user_data=read_data_user()
                    user_data[sname]["admin_ctrl"]=True
                    save_data_user(user_data)

                    admin_message=input("Type your problem: ")
                    user_mess=read_data_admin_notifi()
                    user_mess[sname]["notif"]=admin_message
                    save_data_admin_notifi(user_mess)

                    print("Notification sent to admin wait for responce!!")
                    break


                    

def admin():
    apass=getpass.getpass("Enter the password:")
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

    notif_count=0
    data_nill_check=read_data_admin_notifi()
    for user , info in data_nill_check.items():
        if info.get("notif") != "nill":
            notif_count+=1

    print("1. See data ")
    print("2. Edit data")
    print(f"3. You have {notif_count} messages")

    with open(absolute_path,"r") as f:
            aa=json.load(f)
    
    data=pd.DataFrame.from_dict(aa,orient="index")
    data.reset_index(inplace=True)
    data.rename(columns={"index":"Coustmer names"} ,inplace=True)
    data.index +=1

    while True:
        try:
            aa1=int(input("select [0][1][2][3]: "))
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
                a=input("Want to login again? y/n: ")
                if a=="y":
                    login()

                else:
                    exit()
            else:
                exit()

        elif aa1==3:
            for user , info in data_nill_check.items():
                if info.get("notif") != "nill":
                    print(f"message from {user}")
                    print(f"message is {data_nill_check[user]['notif']}")
                    print("-------------------------------------")
                    admin_w=input("Want to jump to password change? y/n: ")
                    if admin_w=="y":
                        auto_password_change()
                    else:
                        break

        elif aa1==0:
            break

        else:
            print("Choose correctly!!")
            continue

def auto_password_change():
    p_change=input("Enter the name of the client to change password: ")
    user_data_p_change=read_data_user()
    user_notif_p_change=read_data_admin_notifi()

    user_dob_hashed=hashing_password(user_data_p_change[p_change]["DOB"])
    user_data_p_change[p_change]["password"]=user_dob_hashed
    user_data_p_change[p_change]["admin_ctrl"]=False
    user_data_p_change[p_change]["password_type"]="default"

    user_notif_p_change[p_change]["notif"]="nill"

    save_data_user(user_data_p_change)
    save_data_admin_notifi(user_notif_p_change)





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


def user_control():
    with open(absolute_path,"r") as f:
        aa=json.load(f)
        mon1=aa[sname.lower()]["money"]

    print("-"*20)
    print("[1]","\033[31m","Deposit money","\033[0m")
    print("[2]","\033[32m","Withdraw money","\033[0m")
    print("[3]  Change Password")
    print("[4]  Transfer money")
    print("[5]  See Transistion history")
    print("[0]  EXIT")
    print("-"*20) 
    

    while True:
        try:
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
                continue

            
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
                continue

            elif user_choice==3:
                c_password=getpass.getpass("Enter your current password: ")

                with open(absolute_path, "r") as k:
                    p=json.load(k)
                    pcheck=p[sname.lower()]["password"]

                    hash_c_password=hashing_password(c_password)

                if hash_c_password==pcheck:
                    c_password=getpass.getpass("Enter new password: ")
                    hash_c_password=hashing_password(c_password)
                    
                    p[sname]["password"]=hash_c_password

                    with open(absolute_path,"w") as k:
                        json.dump(p,k,indent=4)

                    change_default=read_data_user()
                    change_default[sname]["password_type"]="custom"
                    save_data_user(change_default)

                    print("Password succesfully changed!!!!")
                    print("-"*20)
                    print("Your are logged out login again")
                    login()
                
                continue

            elif user_choice==0:
                exit()

            elif user_choice==4:
                while True:
                    with open(absolute_path,"r") as m:
                        data_load=json.load(m)

                    user_tname=input("Enter the name of the person you want to transfer money to: ")
                    if user_tname in data_load:
                        print("User found !!!")
                        try:
                            amt_t=int(input("Enter the amount to be transferd: "))
                            if data_load[sname]["money"]<amt_t:
                                print("Not enough funds")
                                break
                            
                            else:
                                data_load[sname]["money"]-=amt_t
                                data_load[user_tname]["money"]+=amt_t

                                u_transfer_jason={
                                    "type":"money transfer",
                                    "from":sname,
                                    "to":user_tname,
                                    "amount":amt_t,
                                    "date and time":now
                                }

                                c_transfer_jason={
                                    "type":"money recived",
                                    "from":sname,
                                    "to":user_tname,
                                    "amount":amt_t,
                                    "date and time":now
                                }

                                #uploading the data
                                with open(absolute_path,"w") as k:
                                    json.dump(data_load,k,indent=4)

                                #uploading data to control.json
                                with open(control_j,"r") as k:
                                    his_load=json.load(k)
                                
                                his_load[sname]["history"].append(u_transfer_jason)
                                his_load[user_tname]["history"].append(c_transfer_jason)

                                with open(control_j,"w") as m:
                                    json.dump(his_load,m,indent=4)

                                

                                print("Suscessfuly transfered!!!!!")
                                print("balance left: ",data_load[sname]["money"])
                                print("-"*20)
                                print("[1]","\033[31m","Deposit money","\033[0m")
                                print("[2]","\033[32m","Withdraw money","\033[0m")
                                print("[3]  Change Password")
                                print("[4]  Transfer money")
                                print("[0]  EXIT")
                                break
                        except ValueError:
                            print("Re enter with correct values")
                        
                    
                    else:
                        print("User not found , re enter the name")
                        continue
            elif user_choice==5:
                print(UserTransferData(sname))

        except ValueError:
            print("Re enter with correct place values")
            
def UserTransferData(UserName):
    data = read_data_control()
    username = UserName.lower()

    if username not in data:
        return pd.DataFrame()  # safe empty table

    rows = []

    for txn in data[username]["history"]:
        rows.append({
            "user": username,
            "type": txn["type"],
            "from": txn["from"],
            "to": txn["to"],
            "amount": txn["amount"],
            "date_time": txn["date and time"]
        })

    df = pd.DataFrame(rows)
    return df


        

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