
import random #module 
import os

mots_listes = ['fruits','couleurs','pays'] 
mot_aleatoire=[]               
mot_decomposer =[] 

result=[]
indexlist=[]


x = 0
nbr_chance=5
chance=0

print("Listes:",mots_listes)

def selectMot():
    n = len(mots_listes) ;print(n)
    rnd = random.randint(0,n-1) #renvoie un entier aléatoirement
    mot_aleatoire.append(mots_listes[rnd]) 
    
    print("le mot aleatoire:",mot_aleatoire[0])
    mot_decomposer[:0]= mot_aleatoire[0]
    print("le mot aleatoire décomposer:",mot_decomposer)
    n= len(mot_aleatoire[0])
    print ("nnn",n)
    creation_X(n)

def creation_X(n):
    for i in range(n):
        result.append("X")

#saisi des lettres par l'utilisateur
def saisi_user(nbr_chance):
    while nbr_chance > 0 and nbr_chance <6:
        a=input ('Vous avez '+str(nbr_chance)+' Chances:')
        print("lettre saisie:",a)  
        
        #x= test_appartenance(a,nbr_chance)
        nbr_chance=test_appartenance(a)
      
    return nbr_chance 
print("nmbre de chance",nbr_chance)

def test_appartenance(a2): 
    global nbr_chance 
    
    
    if a2 in mot_decomposer:
        #reinit le tableau d'index
        indexlist=[] 
        for i in range(len(mot_decomposer)) :
            if a2  == mot_decomposer[i]: 
                indexlist.append(i)
           #print(indexlist)
        for j in indexlist:
            #print ("j=",j)
            result[j]=a2
        print('Bien joué :) !!!,voici l''emplacement de ce lettre',indexlist)
        print(result) #liste mise à jour.. 
        os.system('cls' if os.name == 'nt' else 'clear')
        print(result)
        
    else:
        
        nbr_chance = nbr_chance - 1
        print('Chance raté :( il ne vous reste plus que',nbr_chance,'Chance')
              
        print("resultat d 'affichage apres saisi ") 
    return nbr_chance 

selectMot()  
nbr_chance = saisi_user(nbr_chance)




