import random
import string

passwords = {}

try:
    with open("passwords.txt","r") as file:
        for line in file:
            website,pwd = line.strip().split(":")
            passwords[website]=pwd
except:
    pass

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%&"
    password = "".join(random.choice(chars) for _ in range(8))
    return password

while True:
    print("\n---------PERSONAL PASSWORD MANAGER------")
    print("1. Save Password")
    print("2. View Password")
    print("3. Generate Password")
    print("4. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        site = input("Enter Website Name : ")
        pwd = input("Enter Password : ")

        passwords[site] = pwd

        with open("passwords.txt" , "a") as file:
            file.write(f"{site}:{pwd}\n")

        print("Saved!")

    elif choice == "2":
        if not passwords:
            print("No Data")
        else:
            for site, pwd in passwords.items():
               print(site,":",pwd)

    elif choice == "3":
        print("Generated Password", generate_password())   

    elif choice == "4":
        print("Exit..") 
        break

    else:
        print("In-Valid Input !")       




     