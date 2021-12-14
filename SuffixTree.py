from tkinter import *
max_char = 256
mod = 1000
terminal_symbols = []


for i in range(35, max_char):
    if((i>=ord('a') and i<=ord('z')) or (i>=ord('A') and i<=ord('Z'))):
        continue
    else:
        terminal_symbols.append(chr(i))


class SuffixTreeNode():
    def __init__(self):
        self.isLeaf = False
        self.cnt = 0
        self.has_children = False
        self.children = [-1] * max_char
        self.labels = [-1] * max_char
        self.StringSuffixIndices = {}
        self.ReverseStringSuffixIndices = []
        self.SuffixLink = -1
        self.LabelHeight = -1
        self.LeafNumber = 0
        self.start, self.end, self.SuffixIndex = -1, -1, -1

def IsTerminal(x):
    if((ord(x)<=ord('z') and ord(x)>=ord('a')) or (ord(x)<=ord('Z') and ord(x)>=ord('A'))):
        return False
    return True


def FindValue(dict, Value):
    if(Value % mod in dict.keys()):
        for j in dict[Value % mod]:
            if(j == Value):
                return True
    return False



class SuffixTree(str):

    def NewNode(self, start, end, isLeaf = False):
        x = SuffixTreeNode()
        x.isLeaf = isLeaf
        x.start = start
        x.end = end
        #start is start
        #end is lst[end]
        if(start != -1):
            x.SuffixLink = self.Root
        self.Nodes.append(x)
        return len(self.Nodes)-1

    def EdgeLength(self, n):
        if(n == self.Root):
            return 0
        return self.lst[self.Nodes[n].end] - self.Nodes[n].start + 1

    def WalkDown(self, CurrentNode, index):
        #APCFWD
        if(self.ActiveLength >= self.EdgeLength(CurrentNode)):
            self.ActiveLength -= self.EdgeLength(CurrentNode)
            self.ActiveEdge = ord(self.String[index - self.ActiveLength])
            self.ActiveNode = CurrentNode
            return 1
        return 0

    def ExtendSuffixTree(self, pos, str):
        self.LeafEnd = 0
        self.lst[0] = pos
        self.RemainingSuffixCount += 1
        self.LastNewNode = -1
        
        while(self.RemainingSuffixCount > 0):
            if(self.ActiveLength == 0):
                self.ActiveEdge = ord(str[pos])  #APCFALZ
        

            if(self.Nodes[self.ActiveNode].children[self.ActiveEdge] == -1):
        
                self.Nodes[self.ActiveNode].children[self.ActiveEdge] = self.NewNode(pos, self.LeafEnd, True)
                if(self.LastNewNode != -1):
                    self.Nodes[self.LastNewNode].SuffixLink = self.ActiveNode
                    self.LastNewNode = -1
            else :

                self.NextNode = self.Nodes[self.ActiveNode].children[self.ActiveEdge]
                if(self.WalkDown(self.NextNode, pos)): #Walkdown happend
                    continue
                #Rule 3
                if(str[self.Nodes[self.NextNode].start + self.ActiveLength] == str[pos]):
                    if(self.LastNewNode != -1 and self.ActiveNode != self.Root):
                        self.Nodes[self.LastNewNode].SuffixLink = self.ActiveNode
                        self.LastNewNode = -1
                    self.ActiveLength += 1
                    break
                #None of the above happend, we are in middle of the edge and there is no match
                #Adding a new internal node and a leaf
                SplitEnd = self.Nodes[self.NextNode].start + self.ActiveLength - 1
                split = self.NewNode(self.Nodes[self.NextNode].start, SplitEnd + 1)
        
                self.Nodes[self.ActiveNode].children[self.ActiveEdge] = split
                self.Nodes[split].children[ord(str[pos])] = self.NewNode(pos, 0, True)

                self.Nodes[self.NextNode].start += self.ActiveLength
                self.Nodes[split].children[ord(str[self.Nodes[self.NextNode].start])] = self.NextNode
                if(self.LastNewNode != -1):
                    self.Nodes[self.LastNewNode].SuffixLink = split
                self.LastNewNode = split


            self.RemainingSuffixCount -= 1
            if(self.ActiveNode == self.Root and self.ActiveLength > 0):
                #APCFER2C1
                self.ActiveLength -= 1
                self.ActiveEdge = ord(str[pos - self.RemainingSuffixCount + 1])
            elif(self.ActiveNode != self.Root):
                self.ActiveNode = self.Nodes[self.ActiveNode].SuffixLink

    def SetSuffixIndex(self, n, labelheight):
        if(n != -1):
            self.Nodes[n].LabelHeight= labelheight
            leaf = True
            for i in range(max_char):
                child = self.Nodes[n].children[i]
                if(child != -1):
                    leaf = False
                    self.SetSuffixIndex(child, labelheight + self.EdgeLength(child))
                    self.Nodes[n].LeafNumber += self.Nodes[child].LeafNumber
            if(leaf):
                self.Nodes[n].LeafNumber = 1
                self.Nodes[n].SuffixIndex = self.size - labelheight


    def PrintTree(self, str):
        for i in range(len(self.Nodes)):
            print("Node and label ",i, str[self.Nodes[i].start: self.lst[self.Nodes[i].end] + 1])
            print("Suffixlink ", self.Nodes[i].SuffixLink)
            print("Children :")
            for j in range(max_char):
                if(self.Nodes[i].children[j] != -1):
                    print(self.Nodes[i].children[j], chr(j), end=' ')
            print("\n")



    def __init__(self, str):
        self.Nodes = []
        self.NodesIndex = []
        self.LastNewNode , self.ActiveNode = -1, -1
        self.ActiveEdge , self.ActiveLength = -1, 0
        self.lst = []
        self.mylist = []
        self.substring = -1
        self.ans = -1
        self.mid = len(str) // 2
        
        for i in range(2 * len(str)):
            self.lst.append(i - 1)
        
        self.String = str
        self.Root = self.NewNode(-1, -1)
        self.RemainingSuffixCount = 0
        self.LeafEnd = -1
        self.RootEnd = -1
        self.SplitEnd = -1
        self.size = len(str)
        self.ActiveNode = self.Root

        for i in range(len(str)):
            self.ExtendSuffixTree(i, str)
        self.SetSuffixIndex(self.Root, 0)

    def DFS(self, n):
        isLeaf = True
        for i in range(max_char):
            if(self.Nodes[n].children[i] != -1):
                isLeaf = False
                self.DFS(self.Nodes[n].children[i])
        if(isLeaf == True):
            self.mylist.append(self.Nodes[n].SuffixIndex)

    def FindPattern(self, n, pos, pattern):
        if(self.Nodes[n].children[ord(pattern[pos])] == -1):
            return -1
        nxt = self.Nodes[n].children[ord(pattern[pos])]
        st = self.Nodes[nxt].start
        en = self.lst[self.Nodes[nxt].end]
        
        if(len(pattern) - pos <= self.EdgeLength(nxt)):
            for i in range(pos, len(pattern)):
                if(pattern[i] != self.String[st]):
                    return -1
                st += 1
            ##pattern found !
            self.mylist = []
            self.DFS(nxt)
            return self.mylist    
        else:
            for i in range(st, en + 1):
                if(pattern[pos] != self.String[i]):
                    return -1
                pos += 1
            return self.FindPattern(nxt, pos, pattern)

    def RepeatedSubstring(self, n, k, substr):
        if(n == self.Root):
            self.substring = -1
            for i in range(max_char):
                child = self.Nodes[n].children[i] 
                if(child != -1):
                    tmp = self.String[self.Nodes[child].start : self.lst[self.Nodes[child].end] + 1]
                    self.RepeatedSubstring(child, k, substr + tmp)
            self.mylist = []
            if(self.substring != -1):
                self.DFS(self.ans)
                return self.mylist, self.substring
            else:
                return -1
        else:
            if(self.Nodes[n].LeafNumber >= k):
                if(self.substring == -1 or len(self.substring) < len(substr)):
                    self.substring = substr
                    self.ans = n

            for i in range(max_char):
                child = self.Nodes[n].children[i] 
                if(child != -1):
                    tmp = self.String[self.Nodes[child].start : self.lst[self.Nodes[child].end] + 1]
                    self.RepeatedSubstring(child, k, substr + tmp)

    def TrimEdges(self, n):
        isLeaf = True
        if(n != self.Root):
            st = self.Nodes[n].start
            en = self.lst[self.Nodes[n].end]
            for i in range(st, en + 1):
                if(IsTerminal(self.String[i])):
                    self.Nodes[n].end = i + 1
                    break
        for i in range(max_char):
            child = self.Nodes[n].children[i]
            if(child != -1):
                isLeaf = False
                self.TrimEdges(child)
                for j in range(max_char):
                    if(self.Nodes[child].labels[j] == 1):
                        self.Nodes[n].labels[j] = 1
        if(isLeaf):
            en = self.lst[self.Nodes[n].end]
            for j in range(len(terminal_symbols)):
                if(self.String[en] == terminal_symbols[j]):
                    self.Nodes[n].labels[j] = 1
        for i in range(max_char):
            if(self.Nodes[n].labels[i] == 1):
                self.Nodes[n].cnt += 1

    
    def FindLCS(self, n, k, substr):
        if(n == self.Root):
            self.mylist = []
            self.substring = -1
            self.ans = -1
            for i in range(max_char):
                child = self.Nodes[n].children[i]
                st = self.Nodes[child].start
                en = self.lst[self.Nodes[child].end]
                if(child != -1):
                    tmp = self.String[st : en + 1]
                    self.FindLCS(child, k, substr + tmp)
            self.DFS(self.ans)
            if(self.ans != -1):
                return self.mylist, self.substring
            return -1
        else:
            #dont have to check the subtree if it doesnt have more than k different labels
            if(self.Nodes[n].cnt >= k):
                
                if(self.substring == -1 or len(substr)>=len(self.substring)):
                    self.substring = substr
                    self.ans = n

                for i in range(max_char):
                    child = self.Nodes[n].children[i]
                    st = self.Nodes[child].start
                    en = self.lst[self.Nodes[child].end]
                    if(child != -1):
                        tmp = self.String[st : en + 1]
                        self.FindLCS(child, k, substr + tmp)

    def FindLongestPalindrome(self, n, substr):
        if(n == self.Root):
            self.ans = -1
            self.substring = -1
            self.mylist = []
            for i in range(max_char):
                child = self.Nodes[n].children[i]
                if(child != -1):
                    tmp = self.String[self.Nodes[child].start : self.lst[self.Nodes[child].end] + 1]
                    self.FindLongestPalindrome(child, substr + tmp)
            
            if(self.ans == -1):
                return -1, -1
            self.DFS(self.ans)
            return self.mylist, self.substring

        else:
            isLeaf = True
            for i in range(max_char):
                child = self.Nodes[n].children[i]
                if(child != -1):
                    isLeaf = False
                    tmp = self.String[self.Nodes[child].start : self.lst[self.Nodes[child].end] + 1]
                    self.FindLongestPalindrome(child, substr + tmp)
                    for j in self.Nodes[child].StringSuffixIndices:
                        if(j % mod in self.Nodes[n].StringSuffixIndices.keys()):
                            self.Nodes[n].StringSuffixIndices[j % mod].append(j)
                        else:
                            self.Nodes[n].StringSuffixIndices[j % mod] = []
                            self.Nodes[n].StringSuffixIndices[j % mod].append(j)

                    for j in self.Nodes[child].ReverseStringSuffixIndices:
                        self.Nodes[n].ReverseStringSuffixIndices.append(j)
            
            if(isLeaf == True):
                en = self.lst[self.Nodes[n].end]
                if(self.String[en] == '#'):
                    val = self.mid - len(substr) 
                    self.Nodes[n].StringSuffixIndices[val % mod] = []
                    self.Nodes[n].StringSuffixIndices[val % mod].append(val)
                else:
                    self.Nodes[n].ReverseStringSuffixIndices.append(self.mid - len(substr))
                
           
            for ReverseIndex in self.Nodes[n].ReverseStringSuffixIndices:
                StringIndex = self.mid - ReverseIndex - len(substr) - 1
                if(FindValue(self.Nodes[n].StringSuffixIndices, StringIndex)):
                    #Palindrome Found
                    if(self.substring == -1 or len(substr) > len(self.substring)):
                        self.ans = n
                        self.substring = substr

cnt = 0

def MultiLineInput():
    strs = []
    if(len(InputLocationVar.get()) > 0):
        file = open(InputLocationVar.get(), "r")
        my_str = ""
        cnt = 0
        tmp = ""
        for line in file:
            if(line[0] != '>'):
                tmp += line
                if(tmp[len(tmp)-1] == "\n"):
                    tmp = tmp[:-1]
            else:
                #end of previous input
                if(len(tmp) > 0):
                    tmp += terminal_symbols[cnt]
                    my_str += tmp
                    strs.append(tmp)
                    cnt += 1
                    tmp = ""
        #last line of input
        if(len(tmp) > 0):
            tmp += terminal_symbols[cnt]
            my_str += tmp
            strs.append(tmp)
            cnt += 1
        file.close()
        set_output(my_str)
    else:
        tmpinput = InputVar.get()
        my_str = ""
        tmp = ""
        cnt = 0
        new_line_indicator = False
        for char in tmpinput:
            if(char != '\n' and char != ">" and new_line_indicator == False):
                tmp += char
            if(char == '\n' and new_line_indicator == True):
                new_line_indicator = False
            if(char == ">"):
                new_line_indicator = True
                if(len(tmp) > 0):
                    tmp += terminal_symbols[cnt]
                    my_str += tmp
                    strs.append(tmp)
                    cnt += 1
                tmp =""

        if(len(tmp) > 0):
                    tmp += terminal_symbols[cnt]
                    my_str += tmp
                    strs.append(tmp)
                    cnt += 1        
    return my_str, strs

def SingleLineInput():
    if(len(InputLocationVar.get()) > 0):
        file = open(InputLocationVar.get(), "r")
        my_str = ""
        for line in file:
            if(line[0] != '>'):
                my_str += line
                if(my_str[len(my_str) - 1] == "\n"):
                    my_str = my_str[:-1]
        file.close()
    else:
        tmpinput = InputVar.get()
        first_line = True
        my_str = ""
        for char in tmpinput:
            if(char == "\n" and first_line):
                first_line = False
            if(char != "\n" and first_line == False):
                my_str += char
               
    return my_str

def OutputToFile(FileLocation, value):
    file = open(FileLocation, "w")
    file.write(str(value))
    file.close()


def PatternRecognition():
    if((len(InputLocationVar.get()) == 0 and len(InputVar.get()) == 0) or 
        len(OutputLocationVar.get()) == 0 or len(PatternVar.get()) == 0):
        set_output("***Please Check the input***\n")
    else:
        my_str, strings = MultiLineInput()
        pattern = PatternVar.get()
        OutputDestination = OutputLocationVar.get()
        StringTree = SuffixTree(my_str)
        answer = StringTree.FindPattern(StringTree.Root, 0, pattern)
        if(answer == -1):
            set_output("No such pattern found")
            OutputToFile(OutputDestination, "No such pattern found")
        else:
            StringLen = 0
            answer.sort()
            AnswerStr = ""
            AnswerIndex = 0
            for i in range(len(strings)):
                AnswerStr += "Pattern found at string " + str(i + 1) + " in positions:\n"
                if(AnswerIndex == len(answer)):
                    break
                while(answer[AnswerIndex] >= StringLen - 1 and answer[AnswerIndex] <= StringLen + len(strings[i]) - 1):
                    AnswerStr += str(answer[AnswerIndex] - StringLen + 1) + " "
                    AnswerIndex += 1                    
                    if(AnswerIndex == len(answer)):
                        break
                AnswerStr += "\n"
                StringLen += len(strings[i])
            set_output(AnswerStr)
            OutputToFile(OutputDestination, AnswerStr)

def RepeatedSubstring():
    if((len(InputLocationVar.get()) == 0 and len(InputVar.get()) == 0) or 
        len(OutputLocationVar.get()) == 0 or len(KnumberVar.get()) == 0):
        set_output("***Please Check the input***\n")
    else:
        my_str = SingleLineInput()
        my_str += "$"
        OutputDestination = OutputLocationVar.get()
        k = int(KnumberVar.get())
        StringTree = SuffixTree(my_str)
        answer = StringTree.RepeatedSubstring(StringTree.Root, k, "")

        if(answer == -1):
            set_output("No such substring found")
            OutputToFile(OutputDestination, "No such substring found")
        else:
            tmpanswer = answer[1]
            if(IsTerminal(answer[1][len(answer[1]) - 1])):
                tmpanswer = answer[1][:-1]
            AnswerStr = "Substring found is " + tmpanswer + "\n"
            AnswerStr += "Positions found on are :\n"
            for IndexNumber in answer[0]:
                AnswerStr += str(IndexNumber + 1) + " "
            AnswerStr += "\n"
            set_output(AnswerStr)
            OutputToFile(OutputDestination, AnswerStr)

def MultiStringLCS():
    if((len(InputLocationVar.get()) == 0 and len(InputVar.get()) == 0) or 
        len(OutputLocationVar.get()) == 0 or len(KnumberVar.get()) == 0):
        set_output("***Please Check the input***\n")
    else:
        my_str, strings = MultiLineInput()
        OutputDestination = OutputLocationVar.get()
        k = int(KnumberVar.get())
        StringTree = SuffixTree(my_str)
        StringTree.TrimEdges(StringTree.Root)
        answer = StringTree.FindLCS(StringTree.Root, k, "")
        
        if(answer == -1):
            set_output("No common substring found")
            OutputToFile(OutputDestination, "No common substring found")
        else:
            StringLen = 0
            EditAnswer = answer[1]
            if(IsTerminal(EditAnswer[len(EditAnswer) - 1]) == True):
                EditAnswer = EditAnswer[:-1]
            AnswerStr = "LCS is : " + EditAnswer + "\n"
            answer = answer[0]
            answer.sort()
            
            AnswerIndex = 0
            for i in range(len(strings)):
                AnswerStr += "Pattern found at string " + str(i + 1) + " in positions:\n"
                if(AnswerIndex == len(answer)):
                    break
                while(answer[AnswerIndex] >= StringLen - 1 and answer[AnswerIndex] <= StringLen + len(strings[i]) - 1):
                    AnswerStr += str(answer[AnswerIndex] - StringLen + 1) + " "
                    AnswerIndex += 1                    
                    if(AnswerIndex == len(answer)):
                        break
                AnswerStr += "\n"
                StringLen += len(strings[i])

            set_output(AnswerStr)
            OutputToFile(OutputDestination, AnswerStr)


def FindLPS():
    if((len(InputLocationVar.get()) == 0 and len(InputVar.get()) == 0) or 
        len(OutputLocationVar.get()) == 0):
        set_output("***Please Check the input***\n")
    else:
        my_str = SingleLineInput()
        my_str = my_str + "#" + my_str[::-1] + "$"
        #Concat string with it's reverse
        OutputDestination = OutputLocationVar.get()
        StringTree = SuffixTree(my_str)
        StringTree.TrimEdges(StringTree.Root)
        answer = StringTree.FindLongestPalindrome(StringTree.Root, "")

        if(answer[1] == -1):
            set_output("No such substring found")
            OutputToFile(OutputDestination, "No such substring found")
        else:
            AnswerStr = "Substring found is " + answer[1] + "\n"
            AnswerStr += "Positions found are :\n"
            for IndexNumber in answer[0]:
                if(IndexNumber <= len(my_str) / 2 - 2):
                    AnswerStr += str(IndexNumber + 1) + " "
            AnswerStr += "\n"
            set_output(AnswerStr)
            OutputToFile(OutputDestination, AnswerStr)


def make_window():
    win = Tk(className=" Suffix Tree App")
    win.geometry("300x250")
    win.configure(bg="#00394d")

    global InputLocationVar, OutputLocationVar, InputVar, output, KnumberVar, PatternVar, MessageVar, message
    MessageVar = StringVar()
    message = Message(win, textvariable=MessageVar, bg="#00394d", fg="white")
    frame1 = Frame(win, bg="#00394d")
    frame1.pack()

    Label(frame1, text="Input file location", bg="#00394d", fg="white").grid(row=0, column=0, sticky=W)
    InputLocationVar = StringVar()
    InputLocation = Entry(frame1, textvariable=InputLocationVar, width=30, bg="#00394d", fg="red")
    InputLocation.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Output file location", bg="#00394d", fg="white").grid(row=1, column=0, sticky=W)
    OutputLocationVar = StringVar()
    OutputLocation = Entry(frame1, textvariable=OutputLocationVar, width=30, bg="#00394d", fg="red")
    OutputLocation.grid(row=1, column=1, sticky=W)

    Label(frame1, text="Input", bg="#00394d", fg="white").grid(row=2, column=0, sticky=W)
    InputVar = StringVar()
    Input = Entry(frame1, textvariable=InputVar, width=30, bg="#00394d", fg="white")
    Input.grid(row=2, column=1, sticky=W)

    Label(frame1, text="Pattern", bg="#00394d", fg="white").grid(row=3, column=0, sticky=W)
    PatternVar = StringVar()
    Pattern = Entry(frame1, textvariable=PatternVar, width=30, bg="#00394d", fg="white")
    Pattern.grid(row=3, column=1, sticky=W)

    
    Label(frame1, text="K", bg="#00394d", fg="white").grid(row=4, column=0, sticky=W)
    KnumberVar = StringVar()
    Knumber = Entry(frame1, textvariable=KnumberVar, width=10, bg="#00394d", fg="white")
    Knumber.grid(row=4, column=1, sticky=W)
    
    
    frame2 = Frame(win)       
    # Row of buttons
    frame2.pack()
    b1 = Button(frame2, text="Pattern Recognition", command=PatternRecognition, bg="#3399ff")
    b2 = Button(frame2, text="Repeated Substring", command=RepeatedSubstring, bg="#3399ff")
    b3 = Button(frame2, text="LCS", command=MultiStringLCS, bg="#3399ff")
    b4 = Button(frame2, text="LPS", command=FindLPS, bg="#3399ff")
    b1.pack(side=LEFT)
    b2.pack(side=LEFT)
    b3.pack(side=LEFT)
    b4.pack(side=LEFT)
    
    return win



def set_output(str):
    MessageVar.set(str)
    message.pack()


win = make_window()
set_output("")
win.mainloop()


