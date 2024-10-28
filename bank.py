import math
import requests
import json
print("Welcome to online Banking Application")
incorrect_password = 0

def check_incorrect_password():
    global incorrect_password
    incorrect_password += 1
    return incorrect_password

def login():
    username= str(input("Please enter your username: "))
    password= str(input("Please enter you pin: "))
    data = {
        "username":username,
        "password":password
    }
    response = requests.post('http://127.0.0.1:8998/check_login',json=data) 
    resp = response.json()
    if resp['message'] == "login success" and resp['status'] == "OK":
        print('-'*30)
        print(resp['message'])
        print('-'*30)
        name = resp['data'][0]['firstname']
        print("welcome to the online banking application" + " " + name)
        print("please choose the menu down here")
        listmanu = ["1-Deposit","2-Withdraw","3-Transfer","4-Check Balance"]
        for item in listmanu:
            print(item)
        choose = int(input("please enter your number of your choose : "))
        if choose == 1:
            deposit = int(input("Please enter your deposit amount: "))
            data_deposit = {
                "account_number" : resp['data'][0]['account_number'],
                "deposit_amount" : deposit
                }
            response = requests.post('http://127.0.0.1:8998/insert_data_deposit',json=data_deposit) 
            resp_deposit = response.json()
            if resp_deposit['message'] == 'insert data success' and resp['status'] == "OK" :
                print('-'*30)
                print(resp_deposit['message'])
                print('-'*30)
                data_cash_balance = {
                    "account_number": resp['data'][0]['account_number']
                }

                response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
                resp_cash_balance = response.json()
                print("Your current balance is" + " "+str(resp_cash_balance['result']['sum_current_balance']))
            else :
                print('-'*30)
                print("insert not success")
                print('-'*30)
        elif choose == 2:
            amount = int(input("Please enter your withdraw amount: "))
            withdraw_amount = amount*-1
            data_cash_balance = {
                 "account_number": resp['data'][0]['account_number']
            }
            response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
            resp_cash_balance = response.json()
            print(f"your current balance is "+ str(resp_cash_balance['result']['sum_current_balance']))
            if amount > resp_cash_balance['result']['sum_current_balance'] :
                print("your balance is insufficient")
            else:
                insert_data_withdraw = {
                    "account_number" : resp['data'][0]['account_number'],
                    "withdraw_amount" : withdraw_amount
                }
                response = requests.post('http://127.0.0.1:8998/insert_data_withdraw',json=insert_data_withdraw)
                resp_withdraw = response.json()
                if resp_withdraw['status'] == 'OK':
                    print("withdraw success")
                    data_cash_balance = {
                    "account_number": resp['data'][0]['account_number']
                    }
                    response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
                    resp_cash_balance = response.json()
                    print('-'*30)
                    print("your current balance is " + " " + str(f"{resp_cash_balance['result']['sum_current_balance']:.2f}") +" $")
                    print('-'*30)
                else:
                    print("withdraw fail")
        elif choose == 3:
            dest = str(input("Please enter the phone number or email of your destination : "))
            data_check_account = {
                "email":dest,
                "phone_number": dest
            }
            response = requests.post('http://127.0.0.1:8998/check_account',json=data_check_account)
            resp_check_account = response.json()
            if resp_check_account['status'] == "OK":
                tranfer_to = resp_check_account['message'][0]['account_number']
                tranfer_amount =float(input("Please enter your tranfer amount: "))
                data_cash_balance = {
                 "account_number": resp['data'][0]['account_number']
                }
                response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
                resp_cash_balance = response.json()
                print(f"your current balance before tranfer is "+ str(resp_cash_balance['result']['sum_current_balance']))
                if tranfer_amount > resp_cash_balance['result']['sum_current_balance'] :
                    print("your balance is insufficient")
                else:
                    data_deposit = {
                        "account_number" : tranfer_to,
                        "deposit_amount" : tranfer_amount
                    }
                    response = requests.post('http://127.0.0.1:8998/insert_data_deposit',json=data_deposit) 
                    resp_deposit = response.json()
                    print('-'*30)
                    print("tranfer success")
                    print('-'*30)
                    if resp_deposit['status'] == "OK":
                        data_deposit = {
                            "account_number" : resp['data'][0]['account_number'],
                            "deposit_amount" : tranfer_amount *-1 #will deduct money from current account
                        }
                        response = requests.post('http://127.0.0.1:8998/insert_data_deposit',json=data_deposit) 
                        resp_deposit = response.json()
                        data_cash_balance = {
                            "account_number": resp['data'][0]['account_number']
                        }
                        response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
                        resp_cash_balance = response.json()
                        print('-'*30)
                        print(f"your current balance after tranfer is "+ str(resp_cash_balance['result']['sum_current_balance']))
                        print('-'*30)
            else:
                print('-'*30)
                print("account not found")
                print('-'*30)
        elif choose == 4:
            data_cash_balance = {
                 "account_number": resp['data'][0]['account_number']
            }
            response = requests.post('http://127.0.0.1:8998/select_data_cash_balance',json=data_cash_balance)
            resp_cash_balance = response.json()
            print('-'*30)
            print("your account number is"+ " "+(resp_cash_balance['result']['account_number']))
            print('-'*30)
            print("and")
            print('-'*30)
            print("your current balance is " + " " + str(f"{resp_cash_balance['result']['sum_current_balance']:.2f}") +" $")
            print('-'*30)
        else:
            print("Either of your username or pin is wrong")
            print('-'*25)
            print("please enter your username and password again")
            print("3 times limit for putting password")
            print('-'*25)
            check = check_incorrect_password()
            print("incorrect password "+ str(check))
            if check == 3 :
                print('-'*25)
                print ("your account has been suspended please contact bank office")
                print('-'*25)
            elif check >= 4 :
                exit()
            else :
                login() 
        exit()

def mainmenu():
    optionone = int(input("Choose 1 to sign in and choose 2 to log in"))
    if optionone == 1:
        signin()
    elif optionone == 2:
        login()
    else:
        print("Option is not available")
        mainmenu()
    exit()
    
def exit():
    print('-'*25)
    print("Thank you for using this app")
    print('-'*25)
login()