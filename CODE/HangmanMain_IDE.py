#!/usr/bin/python3
from tkinter import Label, Button, Frame, Tk, Entry, PhotoImage, END, Text, TOP, IntVar, Radiobutton
import random
import tkinter.messagebox as msgbox


class Hangman:
    """
    Class used to initialize game of Hangman      
    """

    def __init__(self,
                 secret_word: str,
                 image: PhotoImage):
        """ 
        Initializes the main login window.
        Initializes class Variables.
        :params:
            :secret word: str| A string is designated as secret word with instantiazation of class
            :image: PhotoImage| An Image is inputted into the class
            """

        # defining class variables
        self.frequencies = ['e', 's', 'i', 'a', 'r', 'n', 't', 'o', 'l', 'd', 'c', 'u', 'g', 'p', 'm', 'h', 'b', 'y', 'f', 'k', 'v', 'w', 'z', 'x', 'j', 'q']
        self.icon = image

        self.wordfile = open('../files/words.txt', "r+")
        self.userfile = open("../files/users.txt", "r+")
        self.adminfile = open("../files/admins.txt", "r+")
        self.highscorefile = open("../files/highscores.csv", "r+")
        self.words = self.wordfile.read().split()
        self.usersl = [user.strip().split(",")
                       for user in self.userfile.readlines()]
        self.adminsl = [admin.strip().split(",")
                        for admin in self.adminfile.readlines()]

        self.highscoresl = [highscore.strip().split(",")
                            for highscore in self.highscorefile.readlines()]
        self.users = {name[0]: name[3]
                      for name in self.usersl if self.usersl.index(name) != 0}

        self.admins = {name[0]: name[1]
                       for name in self.adminsl if self.adminsl.index(name) != 0}
        self.highscorers = {
            name[0]: int(name[1]) for name in self.highscoresl}
        self.highscores = list(self.highscorers.values())
        self.s_word = secret_word
        self.guess = 6
        self.warning = 3
        self.guessed_aplha = ""
        # LoginWindow defineds

        self.loginwindow = Tk()
        self.loginwindow.configure(
            background="#323232",
            height=200,
            padx=190,
            pady=90,
            width=200
        )
        self.loginwindow.title("Login or SignUp")
        # Admin Frame
        self.admin_frame = Frame(self.loginwindow)
        self.admin_frame.configure(
            height=200, padx=70, pady=70, width=200, bg="#323232")
        self.adminlabel = Label(self.admin_frame)
        self.adminlabel.configure(
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#F8F8F6",
            text='ADMIN LOGIN')
        self.adminlabel.pack(pady=30, side="top")

        # Admin Entry for username
        self.admin_username = Entry(self.admin_frame)
        self.admin_username.configure(font=("Cartograph CF", 12), width=30)
        _text_ = 'Enter Username'
        self.admin_username.delete("0", "end")
        self.admin_username.insert("0", _text_)
        self.admin_username.pack(pady=3, side="top")

        # Admin Entry for password
        self.admin_password = Entry(self.admin_frame)
        self.admin_password.configure(font=("Cartograph CF", 12), width=30, show="*")
        _text_ = 'Enter Password'
        self.admin_password.delete("0", "end")
        self.admin_password.insert("0", _text_)
        self.admin_password.pack(padx=3, side="top")

        # Admin Submit Button
        self.admin_submit = Button(self.admin_frame)
        self.admin_submit.configure(text='Submit')
        self.admin_submit.pack(pady=17, side="top")
        self.admin_submit.configure(command=self.admin_login)
        self.admin_frame.grid(column=0, padx=30, row=0)

        # Userframe Defined
        self.user_frame = Frame(self.loginwindow)
        self.user_frame.configure(
            height=200, padx=70, pady=70, width=200, bg="#323232")
        self.user_label = Label(self.user_frame)
        self.user_label.configure(
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#F8F8F6",
            text='USER LOGIN')
        self.user_label.grid(column=0, columnspan=2, pady=30, row=0)

        # Entry Field for User Username
        self.user_username = Entry(self.user_frame)
        self.user_username.configure(font=("Cartograph CF", 12), width=30)
        _text_ = 'Enter Username'
        self.user_username.delete("0", "end")
        self.user_username.insert("0", _text_)
        self.user_username.grid(column=0, columnspan=2, padx=3, row=1)

        # Entry Field for User Password
        self.user_password = Entry(self.user_frame)
        self.user_password.configure(font=("Cartograph CF", 12), width=30, show="*")
        _text_ = 'Enter Password'
        self.user_password.delete("0", "end")
        self.user_password.insert("0", _text_)
        self.user_password.grid(column=0, columnspan=2, padx=3, row=2)

        # User Submit button
        self.user_submit = Button(self.user_frame)
        self.user_submit.configure(text='Submit', width=18)
        self.user_submit.grid(column=0, row=3)
        self.user_submit.configure(command=self.user_login)

        # User Register button
        self.user_regis = Button(self.user_frame)
        self.user_regis.configure(text='Register?', width=18)
        self.user_regis.grid(column=1, row=3)
        self.user_regis.configure(command=self.user_register)

        # Grid Settings
        self.user_frame.grid(column=1, padx=33, pady=33, row=0)
        self.user_frame.rowconfigure(1, pad=3)
        self.user_frame.rowconfigure(3, pad=33)
        self.user_frame.columnconfigure(0, pad=3)

    def run(self):
        '''
        Allows main window to run.
        Takes no parameters
        returns: None'''
        self.loginwindow.mainloop()

    def admin_login(self):
        """
        Class method for admin authentication

        returns: None"""
        if self.admin_username.get() in self.admins.keys() and self.admin_password.get() in self.admins.values():
            msgbox.showinfo(title="Successful",
                            message=f"Logged In as {self.admin_username.get()}")
            self.loginwindow.destroy()
            self.admin_interface()

        else:
            msgbox.showerror(
                title="Error", message="Incorrect Username or Password")

    def user_login(self):
        """
        Class method for User login.

        returns: None"""
        self.current_username = self.user_username.get()
        self.current_user_password = self.user_password.get()
        if self.current_username in self.users.keys() and self.current_user_password in self.users.values():
            msgbox.showinfo(title="Successful",
                            message=f"Logged In as {self.user_username.get()}")
            self.loginwindow.destroy()
            self.game()

        else:
            msgbox.showerror(
                title="Error", message="Incorrect Username or Password")

    def user_register(self):
        """
        Class methods for registering a new user

        return: None"""

        # Register Window Initialized
        
        self.register_window = Tk()
        self.register_window.configure(bg="#323232")
        self.register_window.minsize(width=800, height=600)
        # Register Frame for Registering
        self.register_frame = Frame(self.register_window)

        self.register_frame.configure(
            height=200, padx=70, pady=70, width=200, bg="#323232")
        self.registerlabel = Label(self.register_frame)
        self.registerlabel.configure(
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#F8F8F6",
            text='R E G I S T E R')
        self.registerlabel.pack(pady=30, side="top")

        # Register Entry for username
        self.register_username = Entry(self.register_frame)
        self.register_username.configure(font=("Cartograph CF", 12), width=30)
        self.register_username.delete("0", "end")
        self.register_username.insert("0", 'Username')
        self.register_username.pack(pady=3, side="top")

        self.register_firstname = Entry(self.register_frame)
        self.register_firstname.configure(font=("Cartograph CF", 12), width=30)
        self.register_firstname.delete("0", "end")
        self.register_firstname.insert("0", 'First Name')
        self.register_firstname.pack(pady=3, side="top")

        self.register_lastname = Entry(self.register_frame)
        self.register_lastname.configure(font=("Cartograph CF", 12), width=30)
        self.register_lastname.delete("0", "end")
        self.register_lastname.insert("0", 'Last Name')
        self.register_lastname.pack(pady=3, side="top")

        # Register Entry for password
        self.register_password = Entry(self.register_frame)
        self.register_password.configure(font=("Cartograph CF", 12), width=30)
        self.register_password.delete("0", "end")
        self.register_password.insert("0", 'Password')
        self.register_password.pack(padx=3, side="top")

        # Register Submit Button
        self.register_submit = Button(self.register_frame)
        self.register_submit.configure(text='Submit')
        self.register_submit.pack(pady=17, side="top")
        self.register_submit.configure(command=self.add_user)
        self.register_frame.pack()
        self.register_window.mainloop()

    def game(self):
        """
        Main game window initializer. 
        Calls many functions to help in maintaing the game

        returns: None"""
        self.maingame = Tk()
        self.maingame.configure(
            background="#323232",
            width = 244,
            height = 144,
            padx=30,
            pady=30)
        self.maingame.title("Hangman")
        self.alphabet_entry = Entry(self.maingame)
        self.alphabet_entry.configure(font=("Cartograph CF", 25), width=7)
        self.alphabet_entry.grid(column=2, row=0)

        self.alphabet = Label(self.maingame)
        self.alphabet.configure(
            padx=20,
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#F8F8F6",
            text='Enter an alphabet --->')
        self.alphabet.grid(column=1, row=0)

        self.displayword = Label(self.maingame)
        self.displayword.configure(
            background="#323232",
            borderwidth=2,
            font=("Cartograph CF", 14, 'bold'),
            foreground="#F8F8F6",
            text="_ " * len(self.s_word)
        )

        # Defining image of hangman
        self.image1 = PhotoImage(
            file="./images/hangman1.png", master=self.maingame)
        self.image2 = PhotoImage(
            file="./images/hangman2.png", master=self.maingame)
        self.image3 = PhotoImage(
            file="./images/hangman3.png", master=self.maingame)
        self.image4 = PhotoImage(
            file="./images/hangman4.png", master=self.maingame)
        self.image5 = PhotoImage(
            file="./images/hangman5.png", master=self.maingame)
        self.image6 = PhotoImage(
            file="./images/hangman6.png", master=self.maingame)
        self.image7 = PhotoImage(
            file="./images/hangmanloss.png", master=self.maingame)

        self.displayword.grid(row=1, column=1, columnspan=2, padx=30)
        self.guessedlwordslabel = Label(self.maingame)
        self.guessedlwordslabel.configure(
            background="#323232",
            borderwidth=2,
            font=("Cartograph CF", 14, 'bold'),
            foreground="#F8F8F6",
            text=f"The length of the word is {len(self.s_word)}\nGuessed Words:",
            padx=10
        )
        self.guessedlwordslabel.grid(column=1, row=2, columnspan=2)
        self.guessed = Label(self.maingame)
        self.guessed.configure(background="#323232",
                               foreground="#F8F8F6",
                               font=("Cartograph CF", 14, "bold"),
                               text=",".join([self.guessed_aplha]))
        self.guessed.grid(column=1, row=3, columnspan=2)
        self.guessable = Label(self.maingame)
        self.guessable.configure(background="#323232",
            font=("Cartograph CF", 14, "bold"),
            foreground="#F8F8F6",
            text ="Suggested Guesses: " + ','.join(self.goodguesses()))
        self.guessable.grid(column=1, row=4, columnspan=2)
        self.guesses = Label(self.maingame,)
        self.guesses.configure(
            background="#323232",
            font=("Cartograph CF", 14, "bold"),
            foreground="#F8F8F6",
            text=f'Guesses remaining:  {self.guess}')
        self.guesses.grid(column=1, row=5)
        
        self.warnings = Label(self.maingame)
        self.warnings.configure(
            background="#323232",
            font=("Cartograph CF", 14, "bold"),
            foreground="#F8F8F6",
            text=f', Warnings remaining: {self.warning}')
        self.warnings.grid(column=2, row=5)

        self.hangmanimage = Label(self.maingame)
        self.img_hangmanlogo = PhotoImage(file="./images/hangman1.png", master=self.maingame)
        self.hangmanimage.configure(image=self.img_hangmanlogo,padx=5)
        self.hangmanimage.grid(column=0, row=0, rowspan=7)
        self.checkbutton = Button(self.maingame,
                                  text='Guess Letter',
                                  padx=30,
                                  pady=10,
                                  font=("Cartograph CF", 14),
                                  command=self.check_word
                                  )
        self.checkbutton.grid(column=1, row=6, columnspan=2)
        # Binds enter button to the entry box
        self.alphabet_entry.bind("<Return>", lambda call_event: self.check_word()) # here lambda is used to pass the a function such that a function is called by a function
        self.maingame.mainloop()

    def admin_interface(self):
        """
        Admin Window initializer
        is called after authentication from func(admin_login)

        returns: None"""
        # Admin Window Initialized
        self.adminwindow = Tk()
        self.adminwindow.configure(
            background="#323232", height=200, width=200, padx=30, pady=30)
        self.adminwindow.title("Admin Window")

        # Entry Box for Words
        self.wordbox = Entry(self.adminwindow)
        self.wordbox.configure(font=("Cartograph CF", 15))
        self.wordbox.grid(row=1, column=2)
        self.instructions = Label(self.adminwindow)
        self.instructions.configure(
                                 text='Enter words each seperated by a space',
                                  padx=30,
                                  pady=10,
                                  font=("Cartograph CF", 14),
                                  background="#323232",
                                  foreground="#F8F8F6"
        )
        self.instructions.grid(row=2,column=2)
        # Save to file button  for words
        self.save_button = Button(self.adminwindow)
        self.save_button.configure(
            state="normal", text='Save Words', font=("Cartograph CF", 15))
        self.save_button.grid(column=2, ipadx=20, pady=20, row=3)
        self.save_button.configure(command=self.save_words)

        # Text Box for highscores
        self.highscores_txt = Text(self.adminwindow)
        self.highscores_txt.configure(
            font=("Cartograph CF", 12),
            foreground="#323232",
            height=30,
            width=50)
        self.highscores_txt.grid(column=0, row=1, columnspan=2)

        # Words label
        self.Words = Label(self.adminwindow)
        self.Words.configure(
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#f8f8f6",
            text='Words',
            padx=33)
        self.Words.grid(column=2, row=0)

        # Highscore label
        self.Highscores = Label(self.adminwindow)
        self.Highscores.configure(
            background="#323232",
            font=("Cartograph CF", 20),
            foreground="#f8f8f6",
            text='Highscores')
        self.Highscores.grid(column=0, padx=33, pady=2, row=0)

        # Save to file button for Highscores
        self.save_highscore = Button(self.adminwindow)
        self.save_highscore.configure(text='Reset Highscores',
                                      fg="#323232",
                                      font=("Cartograph CF", 15))
        self.save_highscore.grid(column=0, ipadx=20, pady=20, row=3)
        self.save_highscore.configure(command=self.reset_high)
        self.open_highscore = Button(self.adminwindow)
        self.open_highscore.configure(text='Open Highscores',
                                      fg="#323232",
                                      font=("Cartograph CF", 15))
        self.open_highscore.grid(column=1, ipadx=20, pady=20, row=3)
        self.open_highscore.configure(command=self.open_highscores)
        self.adminwindow.rowconfigure(0, pad=33)
        self.adminwindow.mainloop()

    def open_highscores(self):
        """
        Submethod of func(admin_interface).
        Allows opening of highscores:

        returns: None"""
        self.highscorefile = open("../files/highscores.csv", "r+")
        self.high = self.highscorefile.read()
        self.highscores_txt.insert(END, self.high)

    def save_words(self):
        """
        Submethod of func(admin_interface).
        Allows admin to update and save words

        returns: None"""

        additions = self.wordbox.get().split()
        for addition in additions:
            if addition not in self.words:
                msgbox.askokcancel(title="Word Addition",
                                message=f"Added the Word: {addition}")
                self.wordfile.seek(0, 2)
                self.wordfile.write(f" {addition}")
                self.wordfile.flush()
            else:
                msgbox.showerror(title="Word Addition", message=f"The Word: {addition} is already in the file")

    def reset_high(self):
        """
        Submethod of func(admin_interface).
        Allows admin to reset the highscore and delete every highscore"""
        self.highscorefile.truncate(0)
        self.highscorefile.flush()
        self.highscores_txt.delete(1.0, END)
        self.highscores_txt.insert(1.0, "")
        msgbox.showinfo(title='Successfull', message="Reset Higsores")

    def obscureword(self):
        """
        Submethod of func(game).
        Returns a string of displayble word

        returns: str"""
        self.outstr = " ".join(
            f"{i}" if i in self.guessed_aplha else "_" for i in self.s_word
        )
        return self.outstr

    def prep_secret(self):
        """
        Submethod of func(game).
        Returns a string of letters in the form of displaying words.

        returns: str"""
        return " ".join([*self.s_word])

    def add_user(self):
        """
        Submethod of func(user_register).
        Adds the user by taking key details from entry box.

        returns: None """
        
        self.current_username = self.register_username.get()
        firstname = self.register_firstname.get()
        lastname = self.register_lastname.get()
        password = self.register_password.get()
        if self.current_username in self.users.keys():
            msgbox.showerror(
                title="Error", message=self.current_username+" is already a registered user\n\n Try a different username")
        elif len(self.current_username) <= 4:
            msgbox.showerror(
                title="Error", message="Length of username should at least be 4 characters long")
        elif len(password) < 8:
            msgbox.showerror(
                title="Error", message="password should atleast be 8 character long")
        else:

            self.userfile.write(
                f"\n{self.current_username},{firstname},{lastname},{password}")
            self.userfile.flush()
            msgbox.showinfo(title="Successful",
                            message=f"Added the User: {self.current_username}")

            self.register_window.destroy()
            self.loginwindow.destroy()
            self.game()

    def check_word(self):
        
        """
        Submethod of func(game). 
        Takes in the user's guess and checks if it is valid (i.e. a single letter that has not been guessed before).
        It also checks if the guess is in the secret word and updates the game state accordingly (e.g. decrementing the number of guesses remaining).
        The method also checks if the user has won or lost the game and displays appropriate messages.
        The method does not return any value, it only updates the game state and displays messages to the user.
        """

        # get the user's input and lowercase it
        self.G = self.alphabet_entry.get().lower()
        self.alphabet_entry.delete(0, END)
        self.alphabet_entry.insert(0, "")

        # check if the input is a single letter or not
        if len(self.G) != 1:
            msgbox.showerror(
                title="Guess", message="Guesses should be a letter(only one character)!")
            return None

        # check if the letter was already guessed before
        if self.G in self.guessed_aplha:
            msgbox.showerror(title="Guess", message="Already Guessed")
            if self.warning < 1:
                self.guess -= 1
                self.guesses.configure(text=f"  Guesses remaining: {self.guess}")
                if self.guess>=1 : self.displayimage()
            else:
                self.warning -= 1
            self.warnings.configure(text=f"Warnings remaining: {self.warning}")

        # check if the letter is in the secret word
        elif (self.G in self.s_word):
            msgbox.showinfo(
                title="Guess", message=f"Good Job! ' {self.G} ' is in the Word")
            self.guessed_aplha += self.G
            self.guessable.configure(text ="Suggested Guesses: " + ','.join(self.goodguesses()))

        # check if the letter is not in the secret word
        elif (self.G not in self.s_word) and (self.G.isalpha()):
            msgbox.showinfo(title="Guess", message="Too Bad not in the word")
            self.guessed_aplha += self.G
            self.guessable.configure(text ="Suggested Guesses: " + ','.join(self.goodguesses()))
            if self.G in "aeiou":
                self.guess -= 2
            else:
                self.guess -= 1
            self.guesses.configure(text=f"Guesses remaining: {self.guess}")
            if self.guess>=1 : self.displayimage()

        # check if the input is not an alphabet
        else:
            msgbox.showerror(title="Guess", message="We only allow alphabets")
            if self.warning < 1:
                self.guess -= 1
                self.guesses.configure(text=f"Guesses remaining: {self.guess}")
                if self. guess>=1 : self.displayimage()

            else:
                self.warning -= 1
            self.warnings.configure(text=f"Warnings remaining: {self.warning}")
        self.displayword.configure(text=self.obscureword())
        self.guessed.configure(text=",".join([*self.guessed_aplha]))
        self.displayimage()
        # check if the user has run out of guesses
        if self.guess < 1:
            msgbox.showinfo(title="GAME OVER", message="G A M E  O V E R")
            msgbox.showinfo(
                title="Sorry", message=f"The word was: {self.s_word}")
            self.lostgame()
        # check if the user has correctly guessed the secret word
        if self.obscureword() == self.prep_secret():
            msgbox.showinfo(title=f"CONGRAGULATIONS {self.current_username}", message="You Won!")
            self.wongame()
    
    def lostgame(self):
        """
        Submethod of func(check_word).
        Initializes the game loss condition

        returns: None
        """

        decision = msgbox.askretrycancel(
            title="Try Again?", message="Want to Try Again?")
        self.maingame.destroy()
        if decision:
            self.guess = 6
            self.warning = 3
            self.guessed_aplha=""
            self.s_word = secret_word()

            self.game()
        else:
            self.goodbye()

    def wongame(self):
        """
        Submethod of func(check_word).
        Initializes the game Won condition

        returns: None
        """
        # Destroys Maingame window
        self.maingame.destroy()

        # Makes Score
        self.score = self.guess * self.uniques()

        # Won Window made
        self.wonwindow = Tk()
        self.wonwindow.title("Congragulations")
        self.wonwindow.configure(background="#323232", height=200, width=200)
        self.wonwindow.minsize(width=800, height=600)
        self.won = Label(self.wonwindow)
        self.won.configure(
            background="#323232",
            font=("Cartograph CF", 38),
            foreground="#F8F8f6",
            text='YOU WON!')
        self.won.pack(side="top")

        # Score Label
        self.scorelabel = Label(self.wonwindow,
                                background="#323232",
                                font=("Cartograph CF", 38),
                                foreground="#F8F8f6",
                                text=f"YOUR SCORE IS {self.score}")
        if len(self.highscores) == 0 or self.score > int(max(self.highscores)):
            self.scorelabel.configure(
                text=f"CONGRAGULATIONS {self.current_username}! A NEW HIGHSCORE\n SCORE IS {self.score}")

        self.scorelabel.pack()

        # Highscore label
        self.highscorelabel = Label(self.wonwindow,
                                    background="#323232",
                                    font=("Cartograph CF", 38),
                                    foreground="#F8F8f6",
                                    text="Top Highscores")
        self.highscorelabel.pack()

        # Highscore checking and storing
        if len(self.highscores) >= 3 and self.score < min(self.highscores):
            pass
        elif self.score >= int(self.highscorers.get(self.current_username, -1)):
            self.highscorers[self.current_username] = self.score
        elif self.score > min(self.highscores):
            keys = list(self.highscorers.keys())
            del self.highscorers[keys[2]]
            self.highscorers[self.current_username] = self.score
        self.highscores_txt = Text(self.wonwindow)
        self.highscores_txt.configure(
            font=("Cartograph CF", 20),
            background="#323232",
            foreground="#F8F8F6",
            height=10,
            width=20)
        self.save_highscores()
        self.open_highscores()  # opens highscore in the text box
        self.highscores_txt.pack()
        
        dec = msgbox.askyesno(title="Play Again?", message='Do you want to play again?')
        self.wonwindow.destroy()
        if dec:
            self.guess = 6
            self.warning = 3
            self.guessed_aplha=""
            self.s_word = secret_word()
            self.game()
        else:
            self.goodbye()

    def uniques(self):
        """
        Submethod of func(won_game).
        Returns the number of unique alphabets in the secret word

        returns: int
        """

        uni = []
        for i in self.s_word:
            if i not in uni:
                uni += i
        return len(uni)

    def goodbye(self):
        """
        Initializes the GoodBye Screen

        """
        goodbyewindow = Tk()
        goodbyewindow.title("Goodbye")
        goodbyewindow.minsize(width=800, height=600)
        goodbyewindow.configure(background='#323232')

        goodbyelabel = Label(goodbyewindow)
        goodbyelabel.configure(
            text="Thanks For Playing",
            font=("Cartograph CF", 32),
            background="#323232",
            foreground="#F8F8F6")
        goodbyelabel.pack()
        goodbyeimage = PhotoImage(
            master=goodbyewindow, file="./images/goodbye.PNG")
        goodbyeimagelabel = Label(goodbyewindow,
            image=goodbyeimage,
            bd=0)
        goodbyeimagelabel.pack()
        self.wordfile.close()
        self.adminfile.close()
        self.userfile.close()
        self.highscorefile.close()
        goodbyewindow.mainloop()

    def displayimage(self):
        """
        Changes the hangman image after every incorrect guess"""
        self.imag_dict = {'img1': self.image1,
                          'img2': self.image2,
                          'img3': self.image3,
                          'img4': self.image4,
                          'img5': self.image5,
                          'img6': self.image6,
                          'img7': self.image7
                          }
        # uses an alogrithm to find a specific file in accordance to the guesses

        img_select = f"img{abs(self.guess-7)}"
        if abs(self.guess-7)>7:
            self.hangmanimage.configure(image=self.imag_dict['img7'])

        self.hangmanimage.configure(image=self.imag_dict[img_select])

    def save_highscores(self):
        """
        Saves highscores to file by converting dictionary to file lines

        returns: None
        """
        count = 0
        # Sorts the dictionary such that highervalues are printed first
        sorted_dict = dict(sorted(self.highscorers.items(),
                           key=lambda x: x[1], reverse=True))
        # seeks to the starting of the file to allow truncating the whole file
        self.highscorefile.seek(0)
        # clears the whole file
        self.highscorefile.truncate(0)
        self.highscorefile.flush()
        for user, score in sorted_dict.items():
            if count < 3:
                self.highscorefile.write(f"{user},{score}\n")

                self.highscorefile.flush()
                count += 1
    # good guesses based on current gussed letters
    def goodguesses(self):
        hints = [i for i in self.frequencies if i not in self.guessed_aplha]
        if x.get()==0:
            return hints[:5]
        elif x.get()==1:
            return hints[:3]
        elif x.get()==2:
            return ["not avaliable on Hard Difficulty"]
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                               x-----------------------CODE FOR INITIALIZATION OF GAME-----------------------x

# starts the game
def play():
    startingwindow.destroy()
    s_word = secret_word()
    hangman_game = Hangman(s_word,icon)
    hangman_game.run()


def secret_word():
    fileref = open('../files/words.txt')
    words = fileref.read().split(" ")
    if x.get()==0:
        easywords = [word for word in words if len(word)<=5]
        return random.choice(easywords)
    elif x.get()==1:
        mediumwords = [word for word in words if 5<len(word)<=7]
        return random.choice(mediumwords)
    else:
        hardwords = [word for word in words if len(word) > 7]
        return random.choice(hardwords)
# Starting window for the game disconnected from the class
startingwindow = Tk()
startingwindow.configure(bg="#323232", padx=30, pady=20)
startingwindow.title("Welcome To Hangman")
startingwindow.minsize(width=1280, height=1024)
img = PhotoImage(file="./images/hangmanlogo.png")
icon = PhotoImage(file="./images/hangmanicontrue.png")
startingwindow.iconphoto(True, icon)
imagelabel = Label(startingwindow,
                    image=img,
                    state="normal",
                    bd=0, text="Select Difficulty",
                    compound=TOP,
                    bg="#323232",
                    fg="#F8F8F6",
                    font=("Cartograph CF", 14))
imagelabel.pack()

# Difficulty Setting
difficulty = ["Easy", "Medium", "Hard"]

x = IntVar()
easyimage = PhotoImage(file="./images/easy.png",master=startingwindow)
mediumimage = PhotoImage(file="./images/medium.png",master=startingwindow)
hardimage = PhotoImage(file="./images/hard.png",master=startingwindow)
images = [easyimage,mediumimage,hardimage]
for i in range(len(difficulty)):
    radiobutton = Radiobutton(  startingwindow,
                                text = difficulty[i],
                                image=images[i],
                                compound="left",
                                variable=x,
                                value=i,
                                padx=30,
                                pady=10,
                                bg="#323232",
                                fg="#F8F8F6",
                                font=("Cartograph CF", 14),
                                selectcolor='#323232')
    radiobutton.pack()

playbutton = Button(startingwindow,
                    text='Play',
                    padx=30,
                    pady=10,
                    font=("Cartograph CF", 14),
                    command=play)
playbutton.pack()

startingwindow.mainloop()
