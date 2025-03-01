import os
import sys
import subprocess
import random
import requests
import curses
import getpass
import time

# Define Directories
joelscript_folder = "JoelscriptFile"
folders = {
    "storage": os.path.join(joelscript_folder, "storage"),
    "notes": os.path.join(joelscript_folder, "notes"),
    "credentials": os.path.join(joelscript_folder, "credentials"),
    "python": os.path.join(joelscript_folder, "python"),
    "subprocess": os.path.join(joelscript_folder, "subprocess"),
    "cache": os.path.join(joelscript_folder, "cache"),
    "programs": os.path.join(joelscript_folder, "programs"),
    "logs": os.path.join(joelscript_folder, "logs"),
    "chat": os.path.join(joelscript_folder, "chat"),
}

# Ensure Directories Exist
for folder in folders.values():
    os.makedirs(folder, exist_ok=True)

credentials_file = os.path.join(folders["credentials"], "user_credentials.txt")

# Secure Setup & Login
def setup():
    if os.path.exists(credentials_file):
        return login()
    
    print("🔰 Welcome to Joelscript Setup!")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Set a password: ").strip()
    with open(credentials_file, "w") as file:
        file.write(f"{username}\n{password}\n")
    
    print(f"🎉 Setup complete! Welcome, {username}.")
    return username

def login():
    print("🔑 Joelscript Login")
    if not os.path.exists(credentials_file):
        print("No credentials found. Starting setup...")
        return setup()

    with open(credentials_file, "r") as file:
        stored_username, stored_password = file.read().split("\n")[:2]

    while True:
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ").strip()
        if username == stored_username and password == stored_password:
            print(f"✅ Login successful! Welcome back, {username}.")
            return username
        else:
            print("❌ Incorrect username or password. Try again.")

# Easter Egg
def easter_egg():
    print("\n🎉 You've unlocked a secret message!")
    print("🚀 Welcome to Joelscript, where Python meets retro computing!")
    print("🐍 Keep coding, keep innovating!")
    print("\n✨ Hidden Mini-Game: Guess the Lucky Number!")

    # Hidden mini-game
    lucky_number = random.randint(1, 10)
    while True:
        guess = input("🔢 Guess a number between 1-10: ")
        if guess.isdigit() and int(guess) == lucky_number:
            print("🎊 Correct! You're a true Joelscript hacker!")
            break
        else:
            print("❌ Nope, try again!")

# File Manager
def file_manager():
    while True:
        print("\n📂 File Manager")
        files = os.listdir(folders["storage"])
        if not files:
            print("📁 No files found.")
        else:
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
        choice = input("\nOptions: [open] [delete] [back]: ").strip().lower()
        if choice == "back":
            break
        elif choice == "open":
            filename = input("Enter filename to open: ").strip()
            filepath = os.path.join(folders["storage"], filename)
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    print("\n--- File Contents ---\n" + file.read())
            else:
                print("❌ File not found.")
        elif choice == "delete":
            filename = input("Enter filename to delete: ").strip()
            filepath = os.path.join(folders["storage"], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"🗑️ Deleted {filename}")
            else:
                print("❌ File not found.")

# Task Manager
def task_manager():
    while True:
        print("\n🔧 Task Manager - Running Processes")
        os.system("tasklist" if sys.platform == "win32" else "ps aux")
        choice = input("\nOptions: [kill] [back]: ").strip().lower()
        if choice == "back":
            break
        elif choice == "kill":
            pid = input("Enter Process ID to terminate: ").strip()
            try:
                os.kill(int(pid), 9)
                print(f"✅ Process {pid} terminated.")
            except:
                print("❌ Invalid Process ID.")
                
# Notes App
def notes():
    while True:
        print("\n📝 Notes App")
        
        # List all available notes
        files = os.listdir(folders["notes"])
        if not files:
            print("📁 No notes found.")
        else:
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")

        # User options
        choice = input("\nOptions: [new] [open] [edit] [delete] [back]: ").strip().lower()
        if choice == "back":
            break
        elif choice in ["new", "open", "edit", "delete"]:
            filename = input("Enter note name: ").strip() + ".txt"
            filepath = os.path.join(folders["notes"], filename)

        if choice == "new":
            with open(filepath, "w") as file:
                file.write(input("Write your note: ") + "\n")
            print(f"✅ Note saved: {filename}")

        elif choice == "open":
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    print("\n--- Note Contents ---\n" + file.read())
            else:
                print("❌ Note not found.")

        elif choice == "edit":
            if os.path.exists(filepath):
                with open(filepath, "a") as file:
                    file.write("\n" + input("Add to note: ") + "\n")
                print(f"✅ Updated: {filename}")
            else:
                print("❌ Note not found.")

        elif choice == "delete":
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"🗑️ Deleted: {filename}")
            else:
                print("❌ Note not found.")


# Ping Command (Check Network Connection)
def ping():
    hostname = input("Enter website or IP to ping: ").strip()
    response = os.system(f"ping -c 4 {hostname}" if os.name != "nt" else f"ping {hostname}")
    
    if response == 0:
        print(f"✅ {hostname} is reachable.")
    else:
        print(f"❌ {hostname} is unreachable.")

# Wget Command (Download Files from the Internet)
def wget():
    url = input("Enter URL to download: ").strip()
    filename = url.split("/")[-1]  # Extract filename from URL
    save_path = os.path.join("JoelscriptFile", "storage", filename)

    try:
        response = requests.get(url, stream=True)
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        print(f"✅ Download complete! File saved as: {save_path}")
    except Exception as e:
        print(f"❌ Download failed: {e}")


# Selector-Based GUI
def gui(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.mousemask(1)

    menu = ["System Info", "File Manager", "Notes", "Task Manager", "Run Python", "Games", "Chat", "Ping", "Wget", "Exit"]
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(1, w // 2 - len("Joelscript GUI") // 2, "Joelscript GUI", curses.A_BOLD)

        for idx, item in enumerate(menu):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu) // 2 + idx
            if idx == selected:
                stdscr.addstr(y, x, item, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu) - 1:
            selected += 1
        elif key == 10:
            return menu[selected]

# Run GUI
def start_gui():
    while True:
        selection = curses.wrapper(gui)
        if selection == "System Info":
            print("\nJoelscript System Info")
            print(f"- OS: {sys.platform}\n- Python Version: {sys.version}")
            input("\nPress Enter to return...")

        elif selection == "File Manager":
            file_manager()
        elif selection == "Notes":
            notes()
        elif selection == "Task Manager":
            task_manager()
        elif selection == "Run Python":
            run_python_script()
        elif selection == "Games":
            easter_egg()
        elif selection == "Chat":
            chat()
        elif selection == "Ping":
            ping()
        elif selection == "Wget":
            wget()
        elif selection == "Exit":
            break

# Console Mode
def start_console():
    while True:
        cmd = input("Joelscript> ").strip().lower()
        if cmd == "exit":
            break
        elif cmd == "help":
            print("📜 Available Commands: file, notes, tasks, games, chat, easter_egg, exit, ping, wget")
        elif cmd == "file":
            file_manager()
        elif cmd == "notes":
            notes()
        elif cmd == "tasks":
            task_manager()
        elif cmd == "games":
            easter_egg()
        elif cmd == "chat":
            chat()
        elif cmd == "easter_egg":
            easter_egg()
        elif cmd == "ping":
            ping()
        elif cmd == "wget":
            wget()
        else:
            print("❓ Unknown command. Type 'help'.")

# Start Joelscript
def start():
    username = setup()
    mode = input(f"👤 Welcome, {username}! Select mode: [gui] or [console]: ").strip().lower()
    if mode == "gui":
        start_gui()
    else:
        start_console()

start()