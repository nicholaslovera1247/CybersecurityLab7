"""
Nicholas Lovera
CS2660 Lab 7
6/15/24
"""
import sys
import os
import csv
import hashlib
from miner import mining, mining_reward
from datetime import datetime as t


menu_database = {"1" : "Wallet Balance", "2" : "Tranfer CatCoins", "3" : "Quit"}
wallets = {"1" : "wallet1", "2" : "wallet2", "3" : "wallet3"}
transfers = {"1" : "Wallet 1", "2" : "Wallet 2", "3" : "Wallet 3", "4": "Back"}


def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

def last_block():
    try:
        with open("blocks.csv", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lastblock = row
            return lastblock
    except FileNotFoundError:
        print("ERROR")
def wallet_balance():
    validation = True
    while validation:
        print("Welcome to Wallet Balance")
        print("Choose one of your wallets:")
        print("1. Wallet 1")
        print("2. Wallet 2")
        print("3. Wallet 3")
        print("4. Back")
        choice = input("Enter: ")
        if choice == "4":
            validation = False

        elif choice not in wallets.keys():
            print("Invalid choice")
        else:
            try:
                with open("wallets.csv", newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if wallets[choice] == row['wallet']:
                            print(f"{row['balance']} CatCoins")
            except FileNotFoundError:
                print("ERROR! File not found. Contact support")


def wallet_transfer():
    validation1 = True
    while validation1:
        transferdatabase = {'wallet':'balance'}
        updatedcsv = []
        print("Please select source wallet:")
        print("1. Wallet 1")
        print("2. Wallet 2")
        print("3. Wallet 3")
        print("4. Back")
        choice = input("Enter: ")
        if choice == "4":
            validation1 = False
        elif choice not in wallets.keys():
            print("Invalid choice")
        else:
            validation2 = True
            while validation2:
                print("Select a destination wallet:")
                for x in transfers.keys():
                    if choice != x:
                        print(f"{x}. {transfers[x]}")
                choice2 = input("Enter: ")
                if choice2 not in wallets.keys() or choice2 == choice:
                    print("Invalid choice")
                elif choice2 == "4":
                    validation2 = False
                else:
                    validation3 = True
                    while validation3:
                        try:
                            amount = float(input("Enter amount to transfer: "))
                            verification = input(f'Are you sure you want to transfer {amount} CatCoins to {transfers[choice2]}? (y/n): ')
                            if verification.lower() == "y":
                                try:
                                    with open("wallets.csv", newline='') as csvfile:
                                        reader = csv.DictReader(csvfile)
                                        for row in reader:
                                            wallet = row['wallet']
                                            balance = row['balance']
                                            transferdatabase[wallet] = balance
                                except FileNotFoundError:
                                    print("ERROR! File not found. Contact support")
                                if float(transferdatabase[wallets[choice]]) < amount:
                                    print("Insufficient funds")
                                    validation3 = False
                                    validation2 = False
                                else:
                                    transferdatabase[wallets[choice]] = float(transferdatabase[wallets[choice]]) - amount
                                    transferdatabase[wallets[choice2]] = float(transferdatabase[wallets[choice2]]) + amount

                                    get_last_block = last_block()
                                    block_header = f"{get_last_block['previous_hash']},{get_last_block['timestamp']},{get_last_block['nonce']},{get_last_block['current_hash']}"
                                    previous_hash = hash_data(block_header)
                                    block_id = int(get_last_block['block_id']) + 1

                                    nonce, timestamp = mining(previous_hash)

                                    current_block_data = f"{wallets[choice]},{wallets[choice2]},{amount},{block_id}"
                                    current_hash = hash_data(current_block_data)
                                    updated_block_data = f"{wallets[choice]},{wallets[choice2]},{amount},{block_id},{previous_hash},{timestamp},{current_hash},{nonce}\n"

                                    for key in transferdatabase.keys():
                                        updatedcsv.append(f'{key},{transferdatabase[key]}\n')

                                    try:
                                        with open("wallets.csv", 'w', newline='') as csvfile:
                                            csvfile.writelines(updatedcsv)
                                    except FileNotFoundError:
                                        print("ERROR! File not found. Contact support")

                                    try:
                                        with open("blocks.csv", 'a', newline='') as csvfile:
                                            csvfile.writelines(updated_block_data)
                                    except FileNotFoundError:
                                        print("ERROR! File not found. Contact support")

                                    validation3 = False
                                    validation2 = False
                            elif verification.lower() == "n":
                                validation3 = False
                                validation2 = False
                            else:
                                print("Invalid choice")
                        except ValueError:
                            print("Invalid, please put a number")











def interface():
    print("Welcome to CatCoin!\n")

    menu_validation = True
    while menu_validation:
        print("Please select from the following options:")
        print("1. Check Wallet Balance")
        print("2. Transfer CatCoins")
        print("3. Quit CatCoin")
        choice = input("Enter: ")
        if choice not in menu_database.keys():
            print("Invalid choice. Please try again.")
        elif choice == "1":
            wallet_balance()
        elif choice == "2":
            wallet_transfer()
        else:
            validation = True
            while validation:
                choice = input("Are you sure you want to exit CatCoin? y/n: ")
                if choice.lower() == "y":
                    quit()
                elif choice.lower() == "n":
                    validation = False
                else:
                    print("Invalid choice. Please try again.")







if __name__ == "__main__":
    interface()