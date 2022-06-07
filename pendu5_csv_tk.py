import csv, random, os, requests, json
import psycopg2, csv
from pprint import pprint
from tkinter import *
# 

pendu_ascii=['''
     _________
     | 
     |
     |
     | 
     |
     | 
     | 
====================''','''
     _________
     |     |
     |
     |
     |
     |
     |
     | 
====================''','''
     _________
     |     |
     |     O
     |
     | 
     |
     | 
     | 
====================''','''
     _________
     |     |
     |     O
     | x---|---x
     | 
     | 
     | 
     | 
====================''','''
     _________
     |     |
     |     O
     | x---|---x
     |     |
     |  
     | 
     | 
====================''','''
     _________
     |     |
     |     O
     | x---|---x
     |     |
     |    / \ 
     | 
     | 
====================''','''
     _________
     |     |
     |     O
     | x---|---x
     |     |
     |    / \ 
     |  _/   \_
     | 
====================''']



def init_user_word(word):
    '''creates and returns the initial user_word list : a list of _ and - and ' based on word to guess given in parameter'''
    w=[]
    for character in word:
        # replace letters by UNDERSCORE
        if 65<=ord(character)<=90:
            w.append("_")
        # keep APOSTROPHE
        elif ord(character)==39:
            w.append("'")
        # replace all other characters by DASH
        else:
            w.append("-")
    return(w)


def create_list(file):
    '''Takes 3rd row from file in parameter, creates and return a list of str''' 
    file = open('villes_france.csv')
    csvreader = csv.reader(file)
    l = []
    for row in csvreader:
            l.append(row[3])
    file.close()
    return(l)

# create the list of words to guess
words = create_list('villes_france.csv')

# Select a random word in list words, create list "word" with letters from the chosen word 
word=[]
word[:0]=random.choice(words)



# declare empty list for already tried letters
tried=[]
# initiate the user word 
user_word = init_user_word(word)
# errors counter and limit
errors = 0
error_limit = 5


############################################################################################
#
#                           Tkinter and main loop 
#
############################################################################################


# Couleurs 
bg0 = '#333333'
bg1 = '#AEA79F'

# créer une fenêtre 
root = Tk()

# personnaliser la fenêtre
root.title("Pendu")
root.geometry("300x490")
root.resizable(width=True, height=True)
# root.minsize(300,500)
# root.maxsize(300,500)
# root.iconbitmap('pendu.ico')
# root.iconbitmap("/home/nico/Documents/Pendu/pendu.ico")
root.config(background = bg0)
# root.config(background='#AEA79F')

# frames
frame_hangman = Frame(root, bg = bg1 , height=230, width=290)
frame_user_word = Frame(root, bg = bg0 , height= 40, width = 290, padx=5,pady=5)
frame_keyboard = Frame(root, bg = bg1, height = 130 , width = 290,  padx=5,pady=5)
frame_output = Frame(root, bg = bg0, height = 40, width= 290, padx= 5, pady=5)
frame_navigate = Frame(root, bg = bg0, height = 50, width = 290, padx= 5, pady=5)



# labels
label_hangman = Label(frame_hangman,text = pendu_ascii[0], font = ('TlwgTypewriter'), fg = 'white', bg = bg0, justify= LEFT)
label_hangman.pack(fill='both')

label_user_word = Label(frame_user_word, text = user_word, font=('TlwgTypewriter'), fg = 'white', bg = bg0)
label_user_word.pack()

label_output = Label(frame_output, text ="", font=('TlwgTypewriter'), fg = 'white', bg = bg0)
label_output.pack()


# Buttons
buttons = {}

# Keyboard configuration
keys0 = ["A","Z","E","R","T","Y","U","I","O","P"]
keys1 = ["Q","S","D","F","G","H","J","K","L","M"]
keys2 = ["W","X","C","V","B","N"]
# configure columns and rows for frame_keyboard :
for i in range(0,len(keys0)):
    Grid.grid_columnconfigure(frame_keyboard, index=i, weight=1)
for i in range(0,3):
    Grid.grid_rowconfigure(frame_keyboard, index=i, weight=1)


def init_game():

    global tried, errors, error_limit, user_word, word, buttons

    # get new word from DB
    word_str = get_word()
    print("new word :",word_str)
    word=[]
    word[:0]= word_str
    pprint(word)

    # initiate the user word 
    user_word = init_user_word(word)
    pprint(user_word)
    label_user_word.configure(text = user_word)

    # reset buttons
    for key in buttons:
        buttons[key].configure(state = NORMAL)

    # empty list of tried letters
    tried=[]

    # errors counter and limit
    errors = 0

    # reset the hangman
    label_hangman.configure(text=pendu_ascii[0])

    # reset the output
    label_output.configure(text="")






# main loop :
def try_letter(letter):

    try:

        global errors,error_limit,user_word,word, buttons

        # if max errors not reached and letter not null,
        if errors < error_limit and letter:
                        
            # if the letter hasn't been tried yet , 
            if letter not in tried:

                # lock corresponding keyboard button
                buttons[letter].configure(state = DISABLED)

                # add the letter to the list of tried letter
                tried.append(letter)

                # if the letter is in the word to letter , get indexes of all instances of letter in word to letter, with enumerate :
                if letter in word:
    
                    indexes = [i for i, x in enumerate(word) if x == letter]

                    # pprint(indexes)

                    for i in indexes:
                        user_word[i] = letter

                    label_user_word.config(text=user_word)

                # if user letter is NOT in the word (), add it to the TRIED list, increment ERRORS
                else:
                    # compteur du nombre d'erreurs
                    errors += 1
                    label_hangman.config(text=pendu_ascii[errors])
                    label_output.config(text=f"{5-errors} trie(s) remaining...")
                    if errors == error_limit:
                        label_output.config(text="GAME OVER")
                        label_user_word.config(text=word)

                # if user_word matches with word to find, display message for user.
                if user_word == word:
                    label_output.config(text="You won!")
                    label_user_word.config(text=word)
    
    except:
        print("something went wrong...")
        


# Keyboard : declare, configure and grid buttons
row=0
for key_list in [keys0,keys1,keys2]:
    
    # get number of keys on the line, will be used for grid column position
    w = len(key_list)
    for i, k in enumerate(key_list):
        # pass each button's text to a function
        action = lambda x = k: try_letter(x)
        # create the buttons and assign to animal:button-object dict pair
        buttons[k] = Button(frame_keyboard,text=k,font=('TlwgTypewriter',15),width=1, command=action)
        # methode .GRID() renvoie toujours NONE : à appliquer après la déclaration du button!
        buttons[k].grid(column = int((10-w)/2)+i, row=row)
    row += 1



# navigation buttons
button_quit = Button(frame_navigate, text = "Quit", font=('TlwgTypewriter',15), width = 6, command= root.destroy)
button_replay = Button(frame_navigate, text = "Replay", font=('TlwgTypewriter',15), width = 6, command= init_game)
Grid.grid_columnconfigure(frame_navigate, index=0, weight=1)
Grid.grid_columnconfigure(frame_navigate, index=1, weight=1)
button_quit.grid(column=0, row= 0, sticky=NSEW)
button_replay.grid(column=1, row =0, sticky=NSEW)

# keyboard events:
def key_pressed(event):
    letter = event.char.upper()
    if (65 <= ord(letter) <= 90):
        try_letter(letter)
    print(event.char.upper())

frame_keyboard.bind_all("<Key>", key_pressed) 

# pack or grid the frames
frame_hangman.pack()
frame_user_word.pack()
frame_keyboard.pack()
frame_output.pack()
# frame_navigate.grid_propagate(False)
frame_navigate.pack()

# frame_hangman.pack_propagate(0)
# frame_user_word.pack_propagate(0)
# frame_keyboard.grid_propagate(False)
# frame_output.pack_propagate(0)
# frame_navigate.grid_propagate(False)


# afficher la fenêtre
root.mainloop()


