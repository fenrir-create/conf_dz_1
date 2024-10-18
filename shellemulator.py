import os
import tarfile
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def load_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    user_name = root.find("username").text
    tar_path = root.find("tarpath").text
    return user_name, tar_path

class ShellEmulator:
    def __init__(self, username, tar_path):
        self.username = username
        self.tar_path = tar_path
        self.cwd = "/"
        self.file_system = {}
        self.load_tar_file()

    def load_tar_file(self):
        with tarfile.open(self.tar_path, 'r') as tar:
            for member in tar.getmembers():
                self.file_system[member.name] = member

    def ls(self):
        result = []
        for item in self.file_system.keys():
            res = item[2::]
            paths =os.path.join(self.cwd)[1::]
            if(paths in res):
                if(paths==''):
                    if(len(res.split('/'))>1):
                        res=res.split('/')[1]
                    else:
                        res=''
                else:
                    res=res[res.rfind(paths)::]
                if(res not in result):
                    result.append(res)
        return " ".join(sorted(set(result)))

    def cd(self, path):
        new_path = os.path.join(self.cwd, path).rstrip('/') + '/'
        if any(new_path in p for p in self.file_system.keys()):
            self.cwd = new_path
        else:
            return "No such directory"

    def head(self, file_name):
        full_path = os.path.join(self.cwd, file_name).lstrip('/')
        for item in self.file_system.keys():
            if(full_path in item):
                full_path=item
                break
        if full_path in self.file_system and self.file_system[full_path].isfile():
            with tarfile.open(self.tar_path, 'r') as tar:
                file = tar.extractfile(self.file_system[full_path])
                return "".join([file.readline().decode() for _ in range(10)])
        return "File not found"

    def whoami(self):
        return self.username

    def du(self):
        size =0 
        for f in self.file_system:
            size+=os.path.getsize(f)
        return f"Directory size: {size} bytes"

class ShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.window = Tk()
        self.window.title("Shell Emulator")
        self.create_gui()

    def create_gui(self):
        self.output_area = ScrolledText(self.window, height=15, width=80)
        self.output_area.pack()

        self.input_area = Entry(self.window, width=80)
        self.input_area.pack()
        self.input_area.bind("<Return>", self.handle_command)

        self.show_prompt()

    def show_prompt(self):
        self.output_area.insert(END, f"{self.shell.username}@emulator:{self.shell.cwd}$ ")

    def handle_command(self, event):
        command = self.input_area.get()
        self.input_area.delete(0, END)
        self.output_area.insert(END, command + "\n")
        self.execute_command(command)

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        if cmd == "ls":
            output = self.shell.ls()
        elif cmd == "cd" and len(parts) > 1:
            output = self.shell.cd(parts[1])
        elif cmd == "head" and len(parts) > 1:
            output = self.shell.head(parts[1])
        elif cmd == "whoami":
            output = self.shell.whoami()
        elif cmd == "du":
            output = self.shell.du()
        elif cmd == "exit":
            self.window.quit()
            return
        else:
            output = "Unknown command"

        if output:
            self.output_area.insert(END, output + "\n")
        self.show_prompt()

    def run(self):
        self.window.mainloop()


        
if __name__ == "__main__":
    config_file = "config.xml"
    user_name, tar_path = load_config(config_file)
    shell = ShellEmulator(user_name, tar_path)
    gui = ShellGUI(shell)
    gui.run()