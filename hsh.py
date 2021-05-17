import os,shutil,subprocess
welcomemessage = "Welcome to HelliSH"
print(welcomemessage)
path = os.environ["PATH"].split(":") #we *should not* modify system path
home = os.environ["HOME"]
userpath = [] #TODO: save this inbetween sessions?
ps1 = "\n$PWD\n\\_$ "
pwd = home
alias = {"mkcd": ["mkdir $1", "cd $1"]} #TODO: make user creatable
while True:
    cmd = input(ps1.replace("$PWD", pwd).replace(home, "~"))
    splitcmd = cmd.split(" ")
    #shell builtins
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
        os.environ["PWD"] = pwd
    elif splitcmd[0] == "exit":
        print("Thanks for visiting HelliSH.")
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
                print(splitcmd)
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
