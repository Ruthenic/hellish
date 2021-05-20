import os,shutil,subprocess,readline,pathlib,socket
welcomemessage = "Welcome to HelliSH"
print(welcomemessage)
path = os.environ["PATH"].split(":") #we *should not* modify system path
home = os.environ["HOME"]
userpath = [] #TODO: save this inbetween sessions?
ps1 = "[\\u@\\h \\W]$ "
try:
    pwd = os.environ["PWD"]
except:
    pwd = home
    os.environ["PWD"] = pwd
alias = {"mkcd": ["mkdir $1", "cd $1"]}
readline.parse_and_bind('tab: complete')
try:
    readline.read_history_file(home + "/" + ".hellishhistory")
except:
    pass
if not os.path.isfile(home + "/.hellishrc"):
    pathlib.Path(home + "/.hellishrc").touch()
rc = open(home + "/.hellishrc", "r").read().replace("\\033", "\033").split("\n")
def rlGetHistory():
    num_items = readline.get_current_history_length()
    return [readline.get_history_item(i) for i in range(0, num_items)]
def cd(home, splitcmd, pwd):
    if splitcmd[0] == "cd":
        oldpwd = pwd
        if cmd == "cd":
            pwd = home
        elif splitcmd[1].startswith("/"):
            #*probably* an absolute path
            pwd = splitcmd[1]
        else:
            #relative path
            ssd = splitcmd[1].split("/")
            for i in ssd:
                if i == "..":
                    pwd = pwd.replace("/" + pwd.split("/")[-1], "")
                else:
                    pwd += "/" + i
        if not os.path.isdir(pwd):
            print("Directory {} not found and/or is a file!".format(pwd.split("/")[-1]))
            return oldpwd
    return pwd
def parsePrompt(ps1, pwd, home):
    ps1 = ps1.replace("$PWD", pwd).replace(home, "~")
    #convert bashisms of ps1
    #example prompt with bash: "[\u@\h \W]$"
    ps1 = ps1.replace("\\u", os.environ["USER"])
    ps1 = ps1.replace("\\h", socket.gethostname())
    ps1 = ps1.replace("\\W", pwd.split("/")[-1])
    return ps1
for cmd in rc:
    if cmd == "" or cmd.startswith("#"):
        continue
    splitcmd = cmd.split(" ")
    if splitcmd[0] == "cd":
        pwd = cd(home, splitcmd, pwd)
        os.environ["PWD"] = pwd
    elif splitcmd[0] == "ps1":
        ps1 = cmd.replace("ps1 ", "").replace("\\n", "\n")
    elif splitcmd[0] == "alias":
        alias[splitcmd[1]] = cmd.replace(splitcmd[0] + " " + splitcmd[1] + " ", "").split(" && ") #lets go i don't use "&&" for literally anything else in the program
    else:
        isCmdFound = False
        for dire in path:
            try:
                if splitcmd[0] in aliasCmds:
                    raise Exception
                subprocess.run([dire + "/" + splitcmd[0]] + splitcmd[1:], cwd=pwd)
                isCmdFound = True
                break
            except:
                pass
        if not isCmdFound:
            try:
                aliasCmds = alias[splitcmd[0]]
                for aliasCmd in aliasCmds:
                    aliasCmd = aliasCmd.replace("$1", splitcmd[1]).split(" ") #who needs more than one arg
                    if aliasCmd[0] == "cd":
                        if cmd == "cd":
                           pwd = home
                        elif aliasCmd[1].startswith("/"):
                            #*probably* an absolute path
                            pwd = aliasCmd[1]
                        else:
                            #relative path
                            ssd = aliasCmd[1].split("/")
                            for i in ssd:
                                if i == "..":
                                    pwd = pwd.replace("/" + pwd.split("/")[-1], "")
                                else:
                                    pwd += "/" + i
                    else:
                        subprocess.run([dire + "/" + aliasCmd[0]] + aliasCmd[1:], cwd=pwd)
            except:
                print(splitcmd[0] + ": command in .hellishrc not found!")
while True:
    try:
        cmd = input(parsePrompt(ps1, pwd, home)) #example: "[\u@\h \W]\$"" 
    except EOFError:
        print("\nThanks for visiting HelliSH.")
        readline.write_history_file(home + "/" + ".hellishhistory")
        exit()
    except KeyboardInterrupt:
        print("^C")
    readline.add_history(cmd)
    if cmd == "" or cmd.startswith("#"):
        continue
    splitcmd = cmd.split(" ")
    #shell builtins
    if splitcmd[0] == "cd":
        pwd = cd(home, splitcmd, pwd)
        os.environ["PWD"] = pwd
    elif splitcmd[0] == "ps1":
        ps1 = cmd.replace("ps1 ", "").replace("\\n", "\n")
    elif splitcmd[0] == "alias":
        alias[splitcmd[1]] = cmd.replace(splitcmd[0] + " " + splitcmd[1] + " ", "").split(" && ") #lets go i don't use "&&" for literally anything else in the program
    elif splitcmd[0] == "exit":
        print("Thanks for visiting HelliSH.")
        readline.write_history_file(home + "/" + ".hellishhistory")
        exit()
    else:
        isCmdFound = False
        for dire in path:
            try:
                if splitcmd[0] in aliasCmds:
                    raise Exception
                subprocess.run([dire + "/" + splitcmd[0]] + splitcmd[1:], cwd=pwd)
                isCmdFound = True
                break
            except:
                pass
        if not isCmdFound:
            try:
                aliasCmds = alias[splitcmd[0]]
                for aliasCmd in aliasCmds:
                    try:
                        aliasCmd = aliasCmd.replace("$1", splitcmd[1]).split(" ") #who needs more than one arg
                    except:
                        aliasCmd = aliasCmd.split(" ")
                    if aliasCmd[0] == "cd":
                        if cmd == "cd":
                           pwd = home
                        elif aliasCmd[1].startswith("/"):
                            #*probably* an absolute path
                            pwd = aliasCmd[1]
                        else:
                            #relative path
                            ssd = aliasCmd[1].split("/")
                            for i in ssd:
                                if i == "..":
                                    pwd = pwd.replace("/" + pwd.split("/")[-1], "")
                                else:
                                    pwd += "/" + i
                    else:
                        subprocess.run([dire + "/" + aliasCmd[0]] + aliasCmd[1:], cwd=pwd)
            except Exception as e:
                print(str(e))
                print(splitcmd[0] + ": command not found!")
