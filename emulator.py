import os
import tarfile
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

class ShellEmulator:
    def __init__(self, hostname, tar_path, log_path):
        self.hostname = hostname
        self.current_dir = '/'
        self.log_path = log_path
        self.file_system = self.load_file_system(tar_path)
        self.log_actions = []

    def load_file_system(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path='temp_fs')
        return 'temp_fs'

    def log(self, action):
        self.log_actions.append(action)

    def save_log(self):
        root = ET.Element("log")
        for action in self.log_actions:
            entry = ET.SubElement(root, "entry")
            entry.text = action
        tree = ET.ElementTree(root)
        tree.write(self.log_path)

    def ls(self):
        print(" ".join(os.listdir(self.current_dir)))
        self.log(f"Executed ls in {self.current_dir}")

    def cd(self, path):
        new_dir = os.path.join(self.current_dir, path)
        if os.path.isdir(new_dir):
            self.current_dir = new_dir
            self.log(f"Changed directory to {self.current_dir}")
        else:
            print(f"cd: no such file or directory: {path}")

    def mv(self, src, dest):
        src_path = os.path.join(self.current_dir, src)
        dest_path = os.path.join(self.current_dir, dest)
        if os.path.exists(src_path):
            os.rename(src_path, dest_path)
            self.log(f"Moved {src} to {dest}")
        else:
            print(f"mv: cannot stat '{src}': No such file or directory")

    def cal(self):
        print(datetime.now().strftime("%B %Y"))
        self.log("Executed cal")

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_dir} $ ")
            if command == "exit":
                self.save_log()
                break
            elif command.startswith("cd "):
                self.cd(command.split(" ")[1])
            elif command == "ls":
                self.ls()
            elif command.startswith("mv "):
                src, dest = command.split(" ")[1:3]
                self.mv(src, dest)
            elif command == "cal":
                self.cal()
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python emulator.py <hostname> <tar_path> <log_path>")
        sys.exit(1)

    hostname = sys.argv[1]
    tar_path = sys.argv[2]
    log_path = sys.argv[3]

    emulator = ShellEmulator(hostname, tar_path, log_path)
    emulator.run()
