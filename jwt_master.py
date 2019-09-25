#!/usr/bin/env python3

import jwt
import base64
import re
import argparse
from termcolor import colored
from threading import Thread
import time

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


def brute(word, variable, alg, token):
        variable = eval(variable)
        print(colored(f"Trying: {word}", "red"))
        new_jwt = jwt.encode(variable, key=word, algorithm=alg)
        new_jwt = new_jwt.decode("UTF-8")
        if token == new_jwt:
            print(colored(f"[+] Correct Secret Key Found!: {word}", "green"))
            global right
            right = "1"
            print(colored("Now use -f in the script to create\nYour own forged JWT token!\n\n", "blue"))


def send_to_brute(wordlist, variable, alg, token):
    try:
        with open(wordlist, 'r') as list:
            for line in list:
                word = line.strip()
                t1 = Thread(target=brute, args=(word, variable, alg, token,))
                t1.start()
                right = "0"
                if right == "1":
                    break
    except KeyboardInterrupt:
        print(colored("\n\n[-] Ctrl + C Detected Qutting program", "red"))


def decode_jwt(token):
    try:
        print("[+] Decoding")
        time.sleep(1)
        ser = re.search('(.*)(?:\\.)(.*)(?:\\.)(.*)', token)
        decoded1 = base64.b64decode(ser.group(1))
        decoded1 = decoded1.decode("UTF-8")
        print(f"\n{ser.group(1)} |" + colored(f" Type And Algorithm : {decoded1}", "green"))
        decoded2 = base64.b64decode(ser.group(2))
        decoded2 = decoded2.decode("UTF-8")
        print(f"\n{ser.group(2)} |" + colored(f" Data : {decoded2}", "green"))
        signiture = ser.group(3)
        print(f"\n{signiture} :" + colored(" Signture", "green"))
        print("\n------------------------------------------------------")
        choice = input(colored("[+] Brute Force For Secret Key? (y/N) - > ", "red"))
        print("\nNOTE: just press enter to use rockyou.txt")
        wordl = input(colored("[+] Enter wordlist FULL PATH(!) - > ", "blue"))
        if wordl == "":
            wordl = "/usr/share/wordlists/rockyou.txt"
        if choice == "y":
            alg = re.search('(?:"alg":")(.*)(?:")', decoded1)
            alg = alg.group(1)
            send_to_brute(wordl, decoded2, alg, token)
    except KeyboardInterrupt:
        print(colored("\n\n[-] Ctrl + C Detected Qutting program", "red"))
    except:
        print(colored("\n[-] Wordlist could be wrong or one of the following errors.", "red"))
        time.sleep(1)
        print(colored("\n\n[-] Error: Try adding '==' or '=' before the dots in the values which weren't printed", "red"))
        print(colored("Example:\nFrom: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\nTo: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9==", "green"))


def parse():
    parser = argparse.ArgumentParser(description="python3 jwt_forger -d <JWT Token>\npython3 -f \"{'username':'admin','iat':'0'}\" -s <secret_key_word> -a <algorithm>")
    parser.add_argument('-d', dest="decode", help='The JWT token you want to decode')
    parser.add_argument('-s', dest="secret", help='The Secret for the JWT token creation')
    parser.add_argument('-f', dest="forge", help='Forge mode - enter the data you want to store in the forged token')
    parser.add_argument('-a', dest="algorithm", help='The algorithm used for the JWT token')

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


main()
