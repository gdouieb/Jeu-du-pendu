import csv, random, os, requests, json
import psycopg2, csv
from pprint import pprint


os.system('cls' if os.name == 'nt' else 'clear')


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
     |     /\ 
     | 
     | 
====================''','''
     _________
     |     |
     |     O
     | x---|---x
     |     |
     |     /\ 
     |   _/  \_
     | 
====================''']



def init_user_word(word):
    '''creates the initial user_word list : a list of _ and - and ' based on word to guess given in parameter'''
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


def disp(l):
    '''display the blank placeholders for all letters of the selected word'''
    for character in l:
        print(f"{character} ", end="")
    print("")  


def get_word():
    conn = psycopg2.connect(dbname="db_pendu", user="python", password="thonpy", host="localhost") #,port = 5432
    cur = conn.cursor()
    table = "tb_villes"
    
    sql_request = f"SELECT nom_ville FROM {table} ORDER BY RANDOM() LIMIT 1"
    # sql_request = f"select count(id_ville) from {table}"
    cur.execute(sql_request)
    # conn.commit()
    # records = cur.fetchall()
    records = cur.fetchall()


    word = records[0][0]

    cur.close()
    conn.close()
    return(word)

word_str = get_word()
word=[]
word[:0]= word_str


#
# Debug : 
# word=[]
# word[:0]="VIELLENAVE-D'ARTHEZ"
# 


# declare empty list for already tried letters
tried=[]

# initiate the user word 
user_word = init_user_word(word)


errors = 0
error_limit = 6



def user_input(a):
    if (len(a) == 1) and (65 <= ord(a) <= 90):
        return a
    print("I only accept ONE UPPER CASE letter at each round!")

def disp_game_status(errors,tried,lost):    
    '''display game status : errors remaining, letters already tried, optional message'''

    # clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')  
    # print the ascii hangman
    print(pendu_ascii[errors])

    #
    # debug : 
    # print(user_word)
    # print(word)
    #
    
    if not lost:
        disp(user_word)
        print(
            f"{error_limit - errors-1} errors remaining",
            f"letters already tried : {tried}",
            sep="\n"
        )
    else:
        disp(word)
    

def disp_info():
    '''function to get info of a city from the geo.api.gouv website'''
    global word_str
    try:
        url=f"https://geo.api.gouv.fr/communes?nom={word_str}"

        data = requests.get(url)

        json_object = json.loads(data.text)

        # pprint(json_object[0])
        pprint(json_object)

    except:
        print("exception occured")


disp_game_status(errors, tried, False)

# start user input
while not len(word) == 0:


    # user input , only 1 character, only letter# letter.upper()
    letter = ""
    letter = user_input(input("type in 1 letter (no symbols, no accent)").upper())

    # if max errors not reached and letter not null,
    if errors < error_limit and letter:
        
        
        # if the letter hasn't been tried yet , 
        if letter not in tried:

            # add the letter to the list of tried letter
            tried.append(letter)

            # if the letter is in the word to letter , get indexes of all instances of letter in word to letter, with enumerate :
            if letter in word:
   
                indexes = [i for i, x in enumerate(word) if x == letter]

                for i in indexes:
                    user_word[i] = letter

            # if user letter is NOT in the word (), add it to the TRIED list, increment ERRORS
            else:
                # compteur du nombre d'erreurs
                errors += 1
                if errors == error_limit:
                    disp_game_status(errors, tried,True)
                    print("GAME OVER")
                    break

            # if user_word matches with word to find, display message for user.
            if user_word == word:
                disp_game_status(errors, tried, False)
                print("You won!")
                disp_info()
                break

        else:
            print(f"You already tried the letter {letter}.")

        print(f"{5-errors} trie(s) remaining...")

    disp_game_status(errors, tried, False)    

