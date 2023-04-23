#imports
import random
import os
import time
import json
try:
  import fade
except ImportError:
  print("fade is not installed installing...")
  os.system("pip install fade")
  exit()
try:
  import cryptography
  from cryptography.fernet import Fernet
except ImportError:
  print("cryptography is not installed installing...")
  os.system("pip install cryptography")
  exit()

#getting ready for ndb
banner = fade.pinkred("""    _   __              ____               ____  ____ 
   / | / /__  ___  ____/ / /__  __________/ __ \/ __ )
  /  |/ / _ \/ _ \/ __  / / _ \/ ___/ ___/ / / / __  |
 / /|  /  __/  __/ /_/ / /  __(__  |__  ) /_/ / /_/ / 
/_/ |_/\___/\___/\__,_/_/\___/____/____/_____/_____/  
                                                      """)

with open("config.json") as config_file:
  data = json.load(config_file)
  mainpassword = data["mainpass"]

mainpass = "ndb-key-mainpass"


#making the functions
def main():
  os.system("clear")

  file_path = "key.key"
  if os.path.exists(file_path):
    pass_exist = True
  else:
    pass_exist = False

  if pass_exist == True:
    password = mainpassword
  else:
    password = mainpassword

  global fernet

  if not pass_exist and password == mainpass:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open('key.key', 'wb') as f:
      f.write(key)
  elif pass_exist and password == mainpass:
    with open("key.key", 'rb') as f:
      key = f.read()
    fernet = Fernet(key)
  else:
    print(f'[!] Wrong Mainpass')
    exit(0)

  print(banner)
  decision = input("""\n\n1 = create file
2 = read file
3 = delete file
4 = show files
5 = exit
Do you want to create a file or read a file? (1, 2, 3, 4 or 5): """)

  if decision == "1":
    create_file()
  elif decision == "2":
    read_file()
  elif decision == "3":
    del_file()
  elif decision == "4":
    show_files()
  elif decision == "5":
    exit()
  else:
    print("Invalid option selected.")


def get_random_number():
  return random.randint(1000000000, 99999999999999)


def get_user_input():
  return input("what do you want to save?> ")


def create_file():
  random_number = get_random_number()
  user_input = get_user_input()
  filename = f'file-{random_number}.ndb'
  message_bytes = user_input.encode('utf-8')
  encrypted = fernet.encrypt(message_bytes)
  with open(filename, 'w') as f:
    f.write(encrypted.decode('utf-8'))
  print(f"the name of the file is: {filename}, save it!")
  time.sleep(5)


def read_file():
  filename = input("What is the name of the file?> ")
  with open(filename, 'r') as f:
    encrypted_data = f.read().encode('utf-8')
    try:
      decrypted_data = fernet.decrypt(encrypted_data)
      print(decrypted_data.decode('utf-8'))
      time.sleep(5)
    except Exception as e:
      print(f"Error occured: {e}")


def del_file():
  filename = input("What is the name of the File?> ")
  rusure = input(f"Are you Sure you want to delete {filename}? (yes/no)> ")

  if rusure == "yes":
    del_success = os.system(f"rm {filename}")
  elif rusure == "no":
    print("okay.")
  else:
    print("idk")


def show_files():
  #path = os.getcwd()
  #ndb_files = [f for f in os.listdir(path) if f.endswith('.ndb')]
  os.system("ls -a *.ndb")
  time.sleep(5)
  #for file in ndb_files:
  #print(file)


#running the main function
while True:
  main()
