import os,shutil,subprocess,readline
welcomemessage = "Welcome to HelliSH"
print(welcomemessage)
path = os.environ["PATH"].split(":") #we *should not* modify system path
home = os.environ["HOME"]
userpath = [] #TODO: save this inbetween sessions?
ps1 = "\n| \033[0;31m$PWD\033[0m\n\\_$ "
pwd = home
alias = {"mkcd": ["mkdir $1", "cd $1"]} #TODO: make user creatable
readline.parse_and_bind('tab: complete')
try:
    readline.read_history_file(home + "/" + ".hellishhistory")
except:
    pass
def rlGetHistory():
    num_items = readline.get_current_history_length()
    return [readline.get_history_item(i) for i in range(0, num_items)]
def cd(home, splitcmd, pwd):
    if splitcmd[0] == "cd":
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
                    pwd = pwd.replace("/" + pwd.split("/")[len(pwd.split("/"))-1], "")
                else:
                    pwd += "/" + i
    return pwd
while True:
    try:
        cmd = input(ps1.replace("$PWD", pwd).replace(home, "~"))
    except EOFError:
        print("\nThanks for visiting HelliSH.")
        readline.write_history_file(home + "/" + ".hellishhistory")
        exit()
    readline.add_history(cmd)
    splitcmd = cmd.split(" ")
    #shell builtins
    if splitcmd[0] == "cd":
        pwd = cd(home, splitcmd, pwd)
        os.environ["PWD"] = pwd
    elif splitcmd[0] == "ps1":
        ps1 = cmd.replace("ps1 ", "").replace("\\n", "\n")
    elif splitcmd[0] == "exit":
        print("Thanks for visiting HelliSH.")
        readline.write_history_file(home + "/" + ".hellishhistory")
        exit()
    else:
        isCmdFound = False
        for dire in path:
            try:
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
                                    pwd = pwd.replace("/" + pwd.split("/")[len(pwd.split("/"))-1], "")
                                else:
                                    pwd += "/" + i
                    else:
                        subprocess.run([dire + "/" + aliasCmd[0]] + aliasCmd[1:], cwd=pwd)
            except:
                print(splitcmd[0] + ": command not found!")
