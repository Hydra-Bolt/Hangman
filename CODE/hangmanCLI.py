# importing Modules that will be helpful
import random
from tkinter import *
# Importing Files:

usersf = open("files\\users.csv","r+") # opens user file
highscoresf = open("files\\highscores.csv","r+") #opens highscores file 
adminsf = open("files\\admins.csv","r+") #opens admins file 
users = [user.strip().split(",") for user in usersf.readlines()]
admins = [admin.strip().split(",") for admin in adminsf.readlines()]
highscoresl = [highscore.strip().split(",") for highscore in highscoresf.readlines()]


# Converting file read into useful information.
user_names = {name[0]:name[3] for name in users if users.index(name)!=0}
admin_names = {name[0]:name[1] for name in admins if admins.index(name)!=0}
highscorers = {name[0]:name[1] for name in highscoresl if highscoresl.index(name)!=0} 
highscores = [score for name,score in highscorers.items()]
# For Good Guesses
frequencies = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']



#Funtion definitions:
def secret_word():
    fileref = open('files\\words.txt')
    words = fileref.read().split(" ")
    return random.choice(words)
def score(name):
    try:
        return f'{name} has highscore of {highscorers[name]}'
    except:
        return "User not found"
def admin_authenticate(name,password):
    if name in admin_names:
        if admins[1] == password:
            print(f"Logged in as {name}")
        else:
            print("Incorrect Password")
    else:
        print("Admin Not found")
def user_register(name,password,first_name,last_name,email=None):
    resp = [name,first_name,last_name,password,email]
    if resp in user_names:
        return "Already in there"
    usersf.write(resp)
    usersf.flush()
    return f"Added {name}"
def highscore_update(name,score):
    #is checked befor if it is considered to be a new highscore
    resp = [name,score]
    highscoresf.write(resp)
    highscoresf.flush()
    return f"Sucessfully added the High score of {name} with {score} score"
    
def admin_register(name,password):
    if isadmin==True:
        resp = [name,password]
        adminsf.write(resp)
        adminsf.flush()
        return f"Added admin {name}"
def obscure_phrase(secret,guessed):
    outstr = ""
    for i in secret:
        if i in guessed and i not in outstr:
            outstr+=i
        else:
            outstr+="_"
    return outstr
def uni_sword(s_word):
    outlist = ''
    for i in s_word:
        if i in outlist:
            pass
        else:
            outlist+=i
    return outlist

def goodguesses(guessed):
    outlist = [i for i in frequencies if i not in guessed]
    return ','.join(outlist[:5])





#running logic is here
# HANGMANPICS = ['''
#   +---+
#   |  \|
#   O   |
#       |
#       |
#       |
# =========''', '''
#   +---+
#   |  \|
#   O   |
#   |   |
#       |
#       |
# =========''', '''
#   +---+
#   |  \|
#   O   |
#  /|   |
#       |
#       |
# =========''', '''
#   +---+
#   |  \|
#   O   |
#  /|\  |
#       |
#       |
# =========''', '''
#   +---+
#   |  \|
#   O   |
#  /|\  |
#  /    |
#       |
# =========''', '''
#   +---+
#   |  \|
#   O   |
#  /|\  |
#  / \  |
#       |
# =========''',
# "GAME OVER"]
# #initialized the win, at the start set to false
# win = False
# #initialized the variables
# s_word = secret_word()
# c_guesses = 0
# warnings = 3
# guesses = 6
# guessed = ""
# outstr = ""
# disp_word = '_ '*len(s_word)
# #game begun
# print("Hi, welcome to HANGMAN!")
# print('''
#   +---+
#   |  \|
#       |
#       |
#       |
#       |
# =========''')
# #CLI FOR THE USER
# print(f'Your word is {len(s_word)} character long')
# print(f'''Your word is {disp_word}''')
# print(f'You have {warnings} warnings and {guesses} guesses left\n------------------------------------------------------------')
# print(f'Starting Good Guesses: {goodguesses(guessed)} ')
# print(s_word)
# #main game begun
# while guesses>0 and warnings>0:
#     #gets the input of the guess
#     letter = input("Your letter: ").lower()
#     #checks for the presence of letter in the seceret word
#     if len(letter)==1 and letter.isalpha():
#         if letter in s_word and letter not in guessed:
#             guessed+=letter
#             outstr = ""
#             c_guesses = 0
#             for i in s_word:

#                 if i in guessed:
#                     outstr += f' {i}'
#                     c_guesses +=1
#                 else:
#                     outstr+=" _"
#         elif letter in guessed:
#             print("ALREADY GUESSED")
#         else:

#             print("Not in the SECRET WORD")
#             guessed+=letter

#             if letter in "aeiou":
#                 print("VOWEL GUESSED")
#                 guesses-=2
#             else:
#                 guesses-=1
#                 print(HANGMANPICS[abs(guesses-5)])
            
#     else:
#         warnings-=1
#         print("ENTER A LETTER! ")
#     print(f'Your word is {outstr}')
#     print(f'Guessed letters are {guessed}')
#     print(f'You have {warnings} warnings and {guesses} guesses left')
#     print(f'Good Guesses are {goodguesses(guessed)}\n------------------------------------------------------------')
#         #checks if the player has won or not
#     if len(s_word) == c_guesses:
#         print("CONRAGULATIONS!")
#         win = True
#         break

# if win==False:

#     print("LOOSER")
#     print(f"DUMBASS THE WORD WAS {s_word}")
# else:
#     score = guesses * len(uni_sword(s_word))
#     print('SCORE IS ',score)
import Hangman
import imp
import random
def play():
    startingwindow.destroy()
def secret_word():
    fileref = open('../files/words.txt')
    words = fileref.read().split(" ")
    return random.choice(words)
imp.reload(Hangman)
startingwindow= Tk()
startingwindow.config(bg="#323232")
img = PhotoImage(file="F:\\CEP PROJECT\\CODE\\hangmanlogo.png")
print(img)
imagelabel = Label(startingwindow,image=img)
imagelabel.pack()
playbutton = Button(startingwindow, text = 'Play', padx=30, pady = 10, font = ("Cartograph CF", 14), command=play)
playbutton.pack()
startingwindow.mainloop()
s_word =secret_word()
hangman_game = Hangman.Hangman( usersf, 
                                adminsf, 
                                highscoresf, 
                                user_names,
                                admin_names,
                                highscorers,
                                highscores,
                                s_word)
                                
hangman_game.run()
   




