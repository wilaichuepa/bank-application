import math
import requests
import json

print("Welcome to online Banking Application")
incorrect_password = 0

def check_incorrect_password():
    global incorrect_password
    incorrect_password += 1
    return incorrect_password

def show_menu():
    print("Please choose from the menu:")
    listmenu = ["1-Deposit", "2-Withdraw", "3-Transfer", "4-Check Balance", "5-Exit"]
    for item in listmenu:
        print(item)
    return int(input("Please enter the number of your choice: "))

def login():
    username = input("Please enter your username: ")
    password = input("Please enter your pin: ")
    data = {
        "username": username,
        "password": password
    }
    response = requests.post('http://127.0.0.1:8998/check_login', json=data)
    resp = response.json() #call api
    
    if resp['message'] == "login success" and resp['status'] == "OK":
        print('-' * 30)
        print(resp['message'])
        print('-' * 30)
        name = resp['data'][0]['firstname']
        print(f"Welcome to the online banking application, {name}!")
        
        while True:
            choice = show_menu()
            
            if choice == 1:
                deposit = int(input("Please enter your deposit amount: "))
                data_deposit = {
                    "account_number": resp['data'][0]['account_number'],
                    "deposit_amount": deposit
                }
                response = requests.post('http://127.0.0.1:8998/insert_data_deposit', json=data_deposit)
                resp_deposit = response.json()
                if resp_deposit['message'] == 'insert data success' and resp_deposit['status'] == "OK":
                    print('-' * 30)
                    print("Deposit successful.")
                    print('-' * 30)
                    data_cash_balance = {
                        "account_number": resp['data'][0]['account_number']
                    }
                    response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                    resp_cash_balance = response.json()
                    print(f"Your current balance is {resp_cash_balance['result']['sum_current_balance']}")
                else:
                    print('-' * 30)
                    print("Deposit failed.")
                    print('-' * 30)

            elif choice == 2:
                amount = int(input("Please enter your withdraw amount: "))
                withdraw_amount = amount * -1
                data_cash_balance = {
                    "account_number": resp['data'][0]['account_number']
                }
                response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                resp_cash_balance = response.json()
                print(f"Your current balance is {resp_cash_balance['result']['sum_current_balance']}")
                
                if amount > resp_cash_balance['result']['sum_current_balance']:
                    print("Your balance is insufficient.")
                else:
                    insert_data_withdraw = {
                        "account_number": resp['data'][0]['account_number'],
                        "withdraw_amount": withdraw_amount
                    }
                    response = requests.post('http://127.0.0.1:8998/insert_data_withdraw', json=insert_data_withdraw)
                    resp_withdraw = response.json()
                    if resp_withdraw['status'] == 'OK':
                        print("Withdraw successful.")
                        response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                        resp_cash_balance = response.json()
                        print(f"Your current balance is {resp_cash_balance['result']['sum_current_balance']:.2f} $")
                    else:
                        print("Withdraw failed.")
            
            elif choice == 3:
                dest = input("Please enter the phone number or email of your destination: ")
                data_check_account = {
                    "email": dest,
                    "phone_number": dest
                }
                response = requests.post('http://127.0.0.1:8998/check_account', json=data_check_account)
                resp_check_account = response.json()
                
                if resp_check_account['status'] == "OK":
                    tranfer_to = resp_check_account['message'][0]['account_number']
                    transfer_amount = float(input("Please enter your transfer amount: "))
                    data_cash_balance = {
                        "account_number": resp['data'][0]['account_number']
                    }
                    response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                    resp_cash_balance = response.json()
                    print(f"Your current balance before transfer is {resp_cash_balance['result']['sum_current_balance']}")
                    
                    if transfer_amount > resp_cash_balance['result']['sum_current_balance']:
                        print("Your balance is insufficient.")
                    else:
                        data_deposit = {
                            "account_number": tranfer_to,
                            "deposit_amount": transfer_amount
                        }
                        response = requests.post('http://127.0.0.1:8998/insert_data_deposit', json=data_deposit)
                        resp_deposit = response.json()
                        print('-' * 30)
                        print("Transfer successful.")
                        print('-' * 30)
                        
                        if resp_deposit['status'] == "OK":
                            data_withdraw = {
                                "account_number": resp['data'][0]['account_number'],
                                "deposit_amount": transfer_amount * -1  # Deduct money from current account
                            }
                            requests.post('http://127.0.0.1:8998/insert_data_deposit', json=data_withdraw)
                            response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                            resp_cash_balance = response.json()
                            print(f"Your current balance after transfer is {resp_cash_balance['result']['sum_current_balance']}")
                else:
                    print('-' * 30)
                    print("Account not found.")
                    print('-' * 30)

            elif choice == 4:
                data_cash_balance = {
                    "account_number": resp['data'][0]['account_number']
                }
                response = requests.post('http://127.0.0.1:8998/select_data_cash_balance', json=data_cash_balance)
                resp_cash_balance = response.json()
                print('-' * 30)
                print(f"Your account number is {resp_cash_balance['result']['account_number']}")
                print(f"Your current balance is {resp_cash_balance['result']['sum_current_balance']:.2f} $")
                print('-' * 30)

            elif choice == 5:
                print("Thank you for using this app.")
                break

            else:
                print("Invalid choice. Please try again.")

    else:
        print("Either your username or pin is wrong.")
        check = check_incorrect_password()
        print(f"Incorrect password {check} times.")
        
        if check == 3:
            print("Your account has been suspended. Please contact the bank office.")
        elif check >= 4:
            exit()
        else:
            login()

login()