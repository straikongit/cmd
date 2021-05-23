import json
import pickle
import re
import os
from pprint import pprint

class kindaDB():


    def globalVars(self):

        global wordMap
        global commands
        global optionMap
        global goptionMap
        global commandMap
        optionMap = {}
        goptionMap = {}
        wordMap = {}
        commandMap = {}

    def __init__(self,pathToJson):
        self.globalVars()
        self.commands = json.load(open(pathToJson))
        self.commandMap={}
        if len(self.commands):
            for c in self.commands["commands"]:
                self.commandMap.update({int(c["id"]): c })
        self.createIndex()


    def getCommand(self, commandID):
        return self.commandMap.get(int(commandID))

    def getModifiedCommand(self, commandID, colored = True):
        cmd = self.getCommand(commandID)
        if cmd:
            s= cmd["command"]
            options = self.getOptions(int(commandID))
            for option in options:
                if options[option]:
                    if colored == True:
                        s= s.replace("[[" + option + "]]", color.RED +  options[option]  + color.END)
                    else:
                        s= s.replace("[[" + option + "]]",   options[option])
                    #x = re.compile(re.escape("[[" + option  + "]]"), re.IGNORECASE)
                    #s=x.sub( options[option]  , s)
            #global options
            options = self.getGlobalOptions()
            for option in options:
                if options[option]:
                    if colored == True:
                        s= s.replace("[[" + option + "]]", color.RED +  options[option]  + color.END)
                    else:
                        s= s.replace("[[" + option + "]]",   options[option])
            return s


    def getOptions(self, commandID):
        if not commandID in optionMap:
            opt = {}
            cmd = self.getCommand(commandID)
            for option in re.findall(u"\[\[(.+?)\]\]",cmd["command"]):
                opt.update({option.upper() : ""}) 
            return opt
            #optionMap.update({commandID:opt})
        return optionMap[commandID]

    def setOptions(self,commandID,option,value):
        option = option.upper()
        if option in self.getOptions(commandID):
        #if option in optionMap[commandID]:
            optionMap.update({commandID:self.getOptions(commandID)})
            optionMap[commandID][option]=value
        else:
            print option + " not found"

    def getGlobalOptions(self):
        return goptionMap

    def setGlobalOptions(self,option,value):
        global goptionMap
        option = option.upper()
        goptionMap[option]=value
 
    def saveOptions(self, fname):
        with open(fname, "w+") as f:
            m={}
            m["options"]=optionMap
            m["goptions"] = goptionMap

            pickle.dump(m, f)

    def LoadOptions(self, fname):
        global optionMap
        global goptionMap
        with open(fname, "r") as f:
            m=pickle.load(f)
            optionMap = m["options"]
            goptionMap = m["goptions"]



    def search(self, searchTerm):
        """"
            searchterm may consist multiple searchstrings.
            all terms must be found in a command
            searchstrings with a trailing minus are excluded
            arrex=[4]
            a= [1, 2, 3, 4, 5]      searchstring 1
            b = [11, 12, 3, 4,7]    searchstring 2
            list(set(a) & set (b))  returns [3, 4]
            [3, 4] - arrex          returns [3]
        """
           
        arr=[]
        arrex=[]
        for t in searchTerm:
            t = t.lower()
            if t[0] == "-":
                #exclude
                texclude=t[1:]
                if texclude in wordMap.keys():
                    arrex= arrex + wordMap[texclude]
            else:
                if t in wordMap.keys():
                    if len(arr):
                        arr = set(arr) & set(wordMap[t])
                    else:
                        arr = wordMap[t]
                else:
                    arr = []
            
        if len(arr) and len(arrex):
                 arr = set(arr) - set(arrex)
        return sorted(arr)




    def createIndex(self):
        #global wordMap
        global commands
        #wordMap ={}
        uniqueIDs=[]
        for command in self.commands["commands"]:
            if command["id"] in uniqueIDs:
                print "id " + command["id"] + " in cmd.json is not unique"
                exit(0)
            uniqueIDs.append(command["id"])

            words = command["header"] + " " + command["tags"] + " " +  command["command"]
            words =  words.lower()
            words = set(re.split(' |, ',words)) # set() to remove doubles
            for word in words:
                arr = wordMap.get(word.strip())
                if arr:
                    arr.append(command["id"])
                else:
                    arr=[command["id"]]

                wordMap.update({word.strip() : arr})


                #wordMap.update({word.strip() : wordMap.get(word.strip(),[]) +  list(str(command["id"]))})
        #pprint (self.commands)
        #pprint (wordMap)


class color:
    RED         = "\033[1;31m"
    BLUE        = "\033[0;34m"
    CYAN        = "\033[0;36m"
    GREEN       = "\033[1;32m"
    GRAY        = "\033[1;37m"
    BROWN       = "\033[0;33m"
    YELLOW      = "\033[1;33m"
    LIGHTBLUE   = "\033[1;34m"
    LIGHTPURPLE = "\033[1;35m"
    LIGHTCYAN   = "\033[1;36m"
    END         = "\033[0;37m"



#Brown/Orange 0;33     Yellow        1;33
#Blue         0;34     Light Blue    1;34
#Purple       0;35     Light Purple  1;35
#Cyan         0;36     Light Cyan    1;36
#Light Gray   0;37     White         1;37


