import os
import base64
import random
import string

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MASTER_FILE = "master.key"
DATA_FILE = "passwords.txt"
CHECK_TOKEN = b"verified"


# ---------------------------------------------------------------------------
# Key derivation / master password handling
# ---------------------------------------------------------------------------

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Turn a master password + salt into a Fernet-compatible key."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key_bytes = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key_bytes)


def setup_master_password() -> Fernet:
    """First-time setup: create a master password and store salt + check token."""
    print("No master password found. Let's set one up.")
    while True:
        pwd1 = input("Create a master password: ")
        pwd2 = input("Confirm master password: ")
        if pwd1 == pwd2 and pwd1:
            break
        print("Passwords didn't match (or were empty). Try again.")

    salt = os.urandom(16)
    key = derive_key(pwd1, salt)
    fernet = Fernet(key)
    token = fernet.encrypt(CHECK_TOKEN)

    try:
        with open(MASTER_FILE, "wb") as f:
            f.write(base64.urlsafe_b64encode(salt) + b"\n" + token)
    except OSError as e:
        print(f"Could not save master password file: {e}")
        raise SystemExit(1)

    print("Master password set. Please remember it — it cannot be recovered.")
    return fernet


def login() -> Fernet:
    """Load existing master password setup, or create one if missing."""
    if not os.path.exists(MASTER_FILE):
        return setup_master_password()

    try:
        with open(MASTER_FILE, "rb") as f:
            salt_b64 = f.readline().strip()
            token = f.readline().strip()
        salt = base64.urlsafe_b64decode(salt_b64)
    except (OSError, ValueError) as e:
        print(f"Master password file is corrupted or unreadable: {e}")
        raise SystemExit(1)

    for attempt in range(3):
        pwd = input("Enter master password: ")
        key = derive_key(pwd, salt)
        fernet = Fernet(key)
        try:
            fernet.decrypt(token)
            return fernet
        except InvalidToken:
            print(f"Incorrect master password. Attempts left: {2 - attempt}")

    print("Too many failed attempts. Exiting.")
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# Password store
# ---------------------------------------------------------------------------

def load_passwords(fernet: Fernet) -> dict:
    passwords = {}
    if not os.path.exists(DATA_FILE):
        return passwords

    try:
        with open(DATA_FILE, "r") as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                if ":" not in line:
                    print(f"Skipping malformed line {line_num} in {DATA_FILE}")
                    continue
                site, enc_pwd = line.split(":", 1)
                try:
                    pwd = fernet.decrypt(enc_pwd.encode()).decode()
                    passwords[site] = pwd
                except InvalidToken:
                    print(f"Skipping line {line_num}: could not decrypt (wrong key or corrupted).")
    except OSError as e:
        print(f"Could not read {DATA_FILE}: {e}")

    return passwords


def save_all_passwords(fernet: Fernet, passwords: dict):
    try:
        with open(DATA_FILE, "w") as file:
            for site, pwd in passwords.items():
                enc_pwd = fernet.encrypt(pwd.encode()).decode()
                file.write(f"{site}:{enc_pwd}\n")
    except OSError as e:
        print(f"Could not write to {DATA_FILE}: {e}")


def generate_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%&"
    return "".join(random.choice(chars) for _ in range(length))


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main():
    fernet = login()
    passwords = load_passwords(fernet)

    while True:
        print("\n---------PERSONAL PASSWORD MANAGER------")
        print("1. Save Password")
        print("2. View Passwords")
        print("3. Generate Password")
        print("4. Update Password")
        print("5. Delete Password")
        print("6. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            site = input("Enter Website Name: ").strip()
            if not site:
                print("Website name cannot be empty.")
                continue
            pwd = input("Enter Password: ")
            passwords[site] = pwd
            save_all_passwords(fernet, passwords)
            print("Saved!")

        elif choice == "2":
            if not passwords:
                print("No Data")
            else:
                for site, pwd in passwords.items():
                    print(site, ":", pwd)

        elif choice == "3":
            print("Generated Password:", generate_password())

        elif choice == "4":
            site = input("Enter Website Name to update: ").strip()
            if site not in passwords:
                print("Website not found.")
                continue
            new_pwd = input("Enter new password: ")
            passwords[site] = new_pwd
            save_all_passwords(fernet, passwords)
            print("Updated!")

        elif choice == "5":
            site = input("Enter Website Name to delete: ").strip()
            if site not in passwords:
                print("Website not found.")
                continue
            del passwords[site]
            save_all_passwords(fernet, passwords)
            print("Deleted!")

        elif choice == "6":
            print("Exit..")
            break

        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()