from tkinter import *
import time, os, random
class GUI:
    def __init__(self):
        pass

    def CreateWindow(self):
        self.trMode, self.sdMode, self.driveLetter, self.window = 'OFF', 'OFF', (os.getcwd()[0]), Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        Label(self.window, text = 'Login', fg = 'black', font = 'None 15 bold').grid(row = 0, column = 0, sticky = W)
        Label(self.window, text = 'Enter User:', fg = 'black').grid(row = 1, column = 0, sticky = W)
        self.usernameIn = Entry(self.window, width = 40)
        self.usernameIn.grid(row = 2, column = 0, sticky = W)
        Label(self.window, text = 'Enter password:', fg = 'black').grid(row = 3, column = 0, sticky = W)
        self.passwordIn = Entry(self.window, width = 40, show = '*')
        self.passwordIn.grid(row = 4, column = 0, sticky = W)
        Button(self.window, text = 'Submit', width = 6, command = lambda:self.SubmitLogin(self)).grid(row = 5, column = 0, sticky = W)
        self.output = Text(self.window, width = 34, height = 1, wrap = WORD,fg = 'red',font = 'None 10')
        self.output.grid(row = 6, column = 0, columnspan = 2, sticky = W)

    def SubmitLogin(self):       
        found, f, self.username, self.password = False, open('Login Info.txt','r'), self.usernameIn.get(), self.passwordIn.get()
        self.output.delete('1.0', END)
        if self.username == '' or self.password == '':
            self.output.config(fg='red')
            self.output.insert(END, 'Error both fields must be filled in.')
            return
        else:
            for line in f:
                readLogin = (re.search(r'Username: (?P<UsernameRead>[\w\d]+) , Password: (?P<PasswordRead>[\w\d]+)',line)).groupdict()
                if readLogin['UsernameRead'] == self.username and readLogin['PasswordRead'] == self.password:
                    found = True
                    self.output.config(fg = 'green')
                    self.output.insert(END, 'Login Sucessful.')
                    self.window.after(500, lambda: self.WaitAndContinue(self))
                    break
            if found == False:
                self.output.config(fg = 'red')
                self.output.insert(END, 'Login Failed.')
        f.close()

    def WaitAndContinue(self):
        self.window.destroy()
        self.Menu(GUI, returning = False)

    def Menu(self, returning):
        self.custom = False
        if returning == True:
            self.window.destroy()
            try:
                del self.text
            except:
                pass
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        Label(self.window, text='TYPERUNNER', bg='white',fg='black', font='None 15 bold', anchor = CENTER).grid(row=0, column=0)
        Button(self.window, text='Play random text', width=40, command=lambda:self.RunTypeRunner(self)).grid(row=1, column=0, sticky=W)
        Button(self.window, text='Play with a specific text', width=40, command=lambda:self.TextSelection(self)).grid(row=2, column=0, sticky=W)
        Button(self.window, text='Play with custom text', width=40, command=lambda:self.CustomTextEntry(self)).grid(row=3, column=0, sticky=W)
        Button(self.window, text = 'View your scores', width=40, command = lambda:self.DisplayScores(self)).grid(row = 4, column = 0, sticky = W)
        Button(self.window, text = 'Add a text to the database', width=40, command = lambda:self.SaveTextMenu(self)).grid(row = 5, column = 0, sticky = W)
        self.toggleTr = Button(self.window, text = 'TR mode: ' + self.trMode, width=20, fg='blue',bg = 'white', command = lambda:self.ToggleTrMode(self))
        self.toggleTr.grid(row = 6, column = 0, sticky = W)
        self.toggleSd = Button(self.window, text = 'Sudden death mode: ' + self.sdMode, width=20, fg='blue', bg = 'white', command = lambda:self.ToggleSdMode(self))
        self.toggleSd.grid(row = 6, column = 0, sticky = E)
        if self.trMode == 'ON':
            self.toggleTr.config(bg = 'grey')
        if self.sdMode == 'ON':
            self.toggleSd.config(bg ='grey')

    def RunTypeRunner(self):
        try:
            print(self.text)
        except:
            self.PickRandomText(self)
        self.lenText = len(self.text)
        self.totalMoved, self.realCharsTyped, self.correctCharactersTyped, self.realCharsFailed, self.realCharsTyped, self.lenTyped, self.charsTypedWrong, self.charPos,\
                        self.wpm, self.wrongStreak, self.first, self.realAccuracy, self.accuracy, self.textHeight, self.textWidth = 0, 0, 0, 0, 0, 0, 0, 0, 0, False, True, 100, 100, (self.lenText/59) + 1, 50
        self.window.destroy()
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        self.typeRunnerText = Text(self.window, width = self.textWidth, height = self.textHeight, wrap = WORD,fg = 'black',font = 'None 15')
        self.typeRunnerText.grid(row = 1, column = 0, columnspan = 2, sticky = W)
        self.typeRunnerText.insert(END, self.text)
        self.typedText = Entry(self.window, width = 92)
        self.typedText.grid(row = 2, column = 0, sticky = W)
        self.typedText.bind("<Key>", lambda event:self.KeyPressed(self,event))
        self.typedText.bind("<Button-1>", lambda event:self.MouseClicked(self,event))
        self.counter = Label(self.window, text = "WPM: "+str(round(self.wpm)) + "   ACCURACY: " + str(round(self.realAccuracy)) + "%" + "    REAL ACCURACY: " + str(round(self.accuracy)) + "%", font = 'None 15 bold')
        self.counter.grid(row = 0, column = 0, sticky = W)
        self.runnerArea = Canvas(self.window, width = 550, height = 80)
        self.runnerArea.grid(row = 3, column = 0, sticky = W)
        self.runnerGif = PhotoImage(file = r'runner.gif')
        self.runner = self.runnerArea.create_image(0, 0, anchor = NW, image = self.runnerGif)
        rectangle = self.runnerArea.create_rectangle(0, 25, 555, 0, fill = '#7AD746')
        self.runnerArea.move(rectangle, 1, 65)
        self.typeRunnerText.configure(state = 'disabled')
        self.window.after(2000, lambda: self.MoveRunner(self))
        self.window.after(1000, lambda:self.UpdateCounter(self))
        self.window.after(100, lambda:self.CalCounter(self))
          
    def PickRandomText(self):
        rfile = random.choice(os.listdir("Texts\\"))
        f = open('Texts\\' + rfile, 'r')
        self.text = f.read().replace('\n', '')
        f.close()

    def KeyPressed(self,event):
        self.typeRunnerText.configure(state = 'normal')
        if self.first == True:
            print('first')
            self.startTime = time.time()
        self.first = False
        print("pressed", repr(event.char))
        if event.char == self.text[self.charPos] and self.wrongStreak != True:
            self.Highlight(self, 'typedChar')
        elif (event.char != self.text[self.charPos] or self.wrongStreak == True) and event.char != '' and event.char != '\x08' and event.char != '\r':
            if self.sdMode == 'ON':
                self.shouldHaveTyped = self.text[self.charPos]
                self.butYouTyped = event.char
                self.window.destroy()
                self.SuddenDeathFailScreen(self)
                return
            self.Highlight(self, 'wrongChar')
            if self.trMode == 'ON' and self.wrongStreak == False:
                self.wrongStreak = True
                self.wrongCharsLeft = 0
            if self.trMode == 'ON' and self.wrongStreak == True:
                self.wrongCharsLeft += 1 
        elif event.char == '\x08':
            self.Highlight(self, 'backspace')
        elif event.char == '' or event.char == '\r':
            pass
        if self.trMode == 'ON' and self.wrongStreak == True:
            print('wrongCharsLeft' + str(self.wrongCharsLeft))
            if self.wrongCharsLeft == 0:
                self.wrongStreak = False
                self.lenTyped -= 1
        self.typeRunnerText.configure(state = 'disabled')

    def SuddenDeathFailScreen(self):
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        Label(self.window, text = 'You got ' + str(round((self.realCharsTyped / self.lenText) * 100, 1)) + '% of the way through the text without making an error, ',font = 'None 15').grid(row = 0, column = 0, sticky = W)
        Label(self.window, text = 'you typed "' + self.butYouTyped + '" when you should have typed "' + self.shouldHaveTyped  + '".',font = 'None 15').grid(row = 1, column = 0, sticky = W)
        Button(self.window, text = 'Back', width = 10, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 2, column = 0, sticky = W)
        
    def Highlight(self, mode):
        if mode == 'backspace':
            if self.trMode == 'ON' and self.wrongStreak == True:
                self.wrongCharsLeft -= 1        
            if self.wrongStreak == False:
                self.lenTyped -= 1
            self.charPos=self.charPos - 1
            if self.realCharsFailed != 0:
                self.realCharsFailed -= 1
        self.typeRunnerText.tag_remove("wrongChar", "1." + str(self.charPos))
        self.typeRunnerText.tag_remove("typedChar", "1." + str(self.charPos))
        if mode != 'backspace':
            self.typeRunnerText.tag_add(mode, "1." + str(self.charPos))
        self.typeRunnerText.tag_config("typedChar", foreground = "green")
        self.typeRunnerText.tag_config("wrongChar", foreground = "red")
        if mode != 'backspace':
            self.charPos += 1
            if self.wrongStreak == False:
                self.lenTyped += 1
        if mode == 'typedChar':
            self.correctCharactersTyped += 1
            self.realCharsTyped += 1
        if mode == 'wrongChar':
            self.charsTypedWrong += 1
            self.realCharsFailed += 1
                   
    def MouseClicked(self,event):
        self.typedText.focus_set()
        print("clicked at", event.x, event.y)

    def MoveRunner(self):
        toMove = ((self.lenTyped / self.lenText) * 490) - self.totalMoved
        self.totalMoved += toMove
        self.runnerArea.move(self.runner, toMove, 0)
        self.window.after(2000, lambda: self.MoveRunner(self))
        
    def UpdateCounter(self):
        self.counter.config(text = "WPM: "+str(round(self.wpm)) + " ACCURACY: " + str(round(self.realAccuracy, 1)) + "%" + " REAL ACCURACY: " + str(round(self.accuracy, 1)) + "%")
        self.window.after(1000, lambda:self.UpdateCounter(self))

    def CalCounter(self):
        if self.first == False:
            timeSinceStart = time.time() - self.startTime
            try:
                self.wpm = (self.correctCharactersTyped / 5) / (timeSinceStart / 60)
                self.accuracy = (self.correctCharactersTyped / (self.correctCharactersTyped + self.charsTypedWrong)) * 100
                self.realAccuracy = (self.realCharsTyped / (self.realCharsTyped + self.realCharsFailed)) * 100
            except ZeroDivisionError:
                pass
            if self.lenText == self.lenTyped:
                self.window.destroy()
                self.Results(self)
                return
        self.window.after(100, lambda:self.CalCounter(self))

    def TextSelection(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        textNames = os.listdir('Texts\\')
        rowNum = 0
        buttons = {}
        for name in textNames:
            rowNum += 1
            buttons[name] = Button(self.window, text = name[:-4], width = 20, command = lambda name = name:self.SelectText(self, name))
            buttons[name].grid(row = rowNum, column = 0, sticky = W)
        Button(self.window, text = 'Back', width = 20, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = rowNum+1, column = 0, sticky = W)
        print(buttons)

    def SelectText(self,name):
        f = open('Texts\\' + name, 'r')
        self.text = f.read().replace('\n', '')
        self.RunTypeRunner(self)

    def CustomTextEntry(self):
        self.custom = True
        self.window.destroy()
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        Label(self.window, text = 'Enter text here:', bg = 'white',fg = 'black', font = 'None 15 bold').grid(row = 0, column = 0, sticky = W)
        self.CustomText = Text(self.window, width=30, height=10, wrap=WORD,fg='black',font='None 10')
        self.CustomText.grid(row = 1, column = 0, columnspan = 2, sticky = W)
        Button(self.window, text = 'Submit', width = 30, command = lambda:self.retrieveValue(self)).grid(row = 2, column = 0, sticky = W)
        Button(self.window, text = 'Back', width = 30, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 3, column = 0, sticky = W)

    def retrieveValue(self):
        self.text = self.CustomText.get('1.0','end-1c')
        self.RunTypeRunner(self)

    def Results(self):
        self.window = Tk()
        self.window.iconbitmap('runner.ico')
        self.window.title('Typerunner')
        Label(self.window, text = "WPM: " + str(round(self.wpm)), fg = 'black', font = 'None 20').grid(row = 1, column = 0, sticky = W)
        Label(self.window, text = "REAL ACCURACY: " + str(round(self.accuracy, 1)) + '%', fg = 'black', font = 'None 20').grid(row = 2, column = 0, sticky = W)
        Label(self.window, text="ACCURACY: " + str(round(self.accuracy, 1)) + '%', fg = 'black', font = 'None 20').grid(row = 3, column = 0, sticky = W)
        if self.custom != True:
            Button(self.window, text = 'Back', width = 10, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 4, column = 0, sticky = W)
        f = open(self.username + "'s scores.txt", "a+")
        toWrite = "WPM: "+str(round(self.wpm)) + "    ACCURACY: " + str(round(self.realAccuracy, 1)) + "%" + "    REAL ACCURACY: " + str(round(self.accuracy, 1)) + "%    with TR mode " + self.trMode + " and Sudden death mode " + self.sdMode + "    On: " + self.text[:41] + "...\n"
        if self.custom == True:
            Button(self.window, text = 'Save this text in the database', command = lambda: self.SaveTextMenu(self)).grid(row = 4, column = 0, sticky = W)
            Button(self.window, text = 'Back', width = 10, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 5, column = 0, sticky = W)
        f.write(toWrite)
        f.close()

    def SaveTextMenu(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        Label(self.window, text = 'Text name: ', fg = 'black', font = 'None 20').grid(row = 0, column = 0, sticky = W)
        self.textNameEntry = Entry(self.window, width = 40)
        self.textNameEntry.grid(row = 1, column = 0, sticky = W)
        Label(self.window, text = 'Text body: ', fg = 'black', font = 'None 20').grid(row = 2, column = 0, sticky = W)
        self.textBodyEntry = Text(self.window, height=20, width=50, wrap = WORD)
        self.textBodyEntry.grid(row = 3, column = 0, columnspan = 2, sticky = W)
        try:
            self.textBodyEntry.insert(END, self.text)
        except:
            pass
        Button(self.window, text = 'Submit', width = 57, command = lambda:self.SaveText(self)).grid(row = 4, column = 0, sticky = W)
        Button(self.window, text = 'Back', width = 57, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 5, column = 0, sticky = W)

    def SaveText(self):
        textName = self.textNameEntry.get()
        textBody = self.textBodyEntry.get('1.0','end-1c')
        f = open('Texts\\' + textName + '.txt', 'w+')
        f.write(textBody)
        f.close()
        self.Menu(self, returning = True)
    
    def DisplayScores(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title('Typerunner')
        self.window.iconbitmap('runner.ico')
        f = open(self.username + "'s scores.txt", "r+")
        scoreText = f.read()
        scores = Text(self.window, width = 140, height = 10, wrap = WORD,fg = 'black',font = 'None 15')
        scores.grid(row = 1, column = 0, columnspan = 2, sticky = W)
        scores.insert(END, scoreText)
        scores.config(state = 'disabled')
        Button(self.window, text = 'Back', width = 10, bg = 'light blue', command = lambda: self.Menu(self, returning = True)).grid(row = 2, column = 0, sticky = W)
        f.close()

    def ToggleTrMode(self):
        if self.trMode == 'OFF':
            self.toggleTr.config(text = 'TR mode: ON')
            self.trMode = 'ON'
            self.toggleTr.config(bg = 'grey')
        else:
            self.toggleTr.config(text = 'TR mode: OFF')
            self.trMode = 'OFF'
            self.toggleTr.config(bg = 'white')

    def ToggleSdMode(self):
        if self.sdMode == 'OFF':
            self.toggleSd.config(text = 'Sudden death mode: ON')
            self.sdMode = 'ON'
            self.toggleSd.config(bg = 'grey')
        else:
            self.toggleSd.config(text = 'Sudden death mode: OFF')
            self.sdMode = 'OFF'
            self.toggleSd.config(bg = 'white')                               

GUI.CreateWindow(GUI)
        

