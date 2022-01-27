# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math;
import os;
import time;
import random;


#-----------------------------------------------------------------------------------------
#Helper functions

def split(word):
    return [char for char in word]

def choose_e(array_E):
    #helps choose a public exponents out of the choices in the array
    
    entered = -1
    
    while(entered < 1):
        entered = int(input("Please enter a public key from the choices provided below: "))    
        if (entered in array_E):
            return int(entered)
        else:
            entered = -1
            print("Value not allowed, please enter again from the choices: ", array_E)
    

def menuPublicUser(e, n, sigVerify):
    #options for a public user to encrypt text for owner/verify digital signature
    

    print(sigVerify)
    valid = True
    print("\nPublic Key: (e =", e, ", n =", n,")") 
    print("\na. encrypt text for owner\nb. Verify digital signature sent by Owner\nc. Exit\n")
    while(valid):
        choice = input("Please enter a, b, or c only: ")
        if((choice != 'a') and (choice != 'b') and (choice != 'c')):
            print("Error, retry a valid character")
        else:
            valid = False
    #encrypt for owner
    if(choice == "a"):
        textTo_Send = input("Please enter text to encrypt and send to Owner: ")
        print("Message sent, Exiting...")
        time.sleep(2)
        return encrypt(textTo_Send, e, n)
    #sign for public
    elif(choice == "b"):
        if(sigVerify):
            sigText = decrypt(sigVerify, e, n)
            toPrint = "".join(sigText)
            print("Signature: ", toPrint)
            print("Exiting in 5 sec...")
            time.sleep(5)
            return sigVerify
        #no signature from owner to verify
        else:
            print("no signature to verify, returning to menu in 3 sec...")
            time.sleep(3)
            menuPublicUser(e, n, sigVerify)
    else:
        print("Exiting...")
        return []
        
    
def menuOwner(e, d, n, cipherReceived):
    #options for owner(private) user to digitally sign or decrypt messages
    
    print(cipherReceived)
    #checkError = "".join(cipherReceived))
    valid = True
    print("\nPublic Key: (e =", e, ", n =", n,")") 
    print("\na. sign message for public\nb. decrypt message received\nc. Exit\n")
    while(valid):
        choice = input("Please enter a, b, or c only: ")
        if((choice != 'a') and (choice != 'b') and (choice != 'c')):
            print("Error, retry a valid character")
        else:
            valid = False
    #encrypt and send        
    if(choice == "a"):
        textTo_Send = input("Please enter text to sign and send to public users: ")
        print("Message sent, Exiting...")
        time.sleep(2)
        return encrypt(textTo_Send, d, n)
    #decrypt the received
    elif(choice == "b"):
        if(cipherReceived):
            MessageText = decrypt(cipherReceived, d, n)
            toPrint = "".join(MessageText)
            print("Message: ", toPrint)
            print("Exiting in 5 sec...")
            time.sleep(5)
            return cipherReceived
        #nothing to encrypt/decrypt
        else:
            print("no message to decrypt, returning to menu in 3 sec...")
            time.sleep(3)
            menuOwner(e, d, n, cipherReceived)
    else:
        print("Exiting...")
        return []
        
    
    
    
    
    
    
#------------------------------------------------------------------------------------------
#Prime Number Generator

def getLargePrimeNum():
    for i in range(40): # Generate until it finds a number that passes Fermat's Theorem
        x = random.randint(350, 1000)    
        if (2 << x - 2) % x == 1: # Test random number to see if it passes Fermat's Theorem
            print(x, 'Is prime because it passes the theorem\n')
            break;  # Stop generating numbers
    return x

def getSmallPrimeNum():
    for i in range(40): # Generate until it finds a number that passes Fermat's Theorem
        x = random.randint(1, 300)    
        if (2 << x - 2) % x == 1: # Test random number to see if it passes Fermat's Theorem
            print(x, 'Is prime because it passes the theorem\n')
            break;  # Stop generating numbers
    return x
    
def checkPrime(potentialPrime):
   #check if the psuedoprime number is statistically prime
   check_k = 0
   valid = True
   passed = False
   ratio = 0
   failed = 0


   while(valid and (failed != 10)): 
       x = random.randint(1, potentialPrime - 1)    #pick out random numbers
       if(((pow(x,potentialPrime-1)) % potentialPrime) == 1): # Test random number to see if it passes Fermat's Theorem
           check_k = check_k + 1
           temp = float(2**check_k)
           ratio = float(1.0/(temp))
           if(ratio < .05): #less than 5 percent chance of not being prime
               valid = False
               passed = True
               break;  # Stop generating number
       else:
           valid = True
           failed += 1
           
   
   return passed

#------------------------------------------------------------------------------------------
#Key Generation


#helper function - extended Euclid's algorithm
def extended_gcd(a, b):
    if (b == 0):
        return (1, 0, a)
    
    (x, y, d) = extended_gcd(b, a%b)

    toReturn = (y, x - (a//b)*y, d)


    return toReturn


#generate public key: e (public exponent)
def publicKey_generate(totient):
    #return an integer(e) such that gcd(e, totient) = 1
    
    potential_E = []
    count = 0

    
    while(count < 20):        #generate 20 random potential e - (public key) 
        x = random.randint(2, totient-1)       
        if(math.gcd(x,totient) == 1):
            potential_E.append(x)
            count += 1
           
        
            
    return potential_E
    


#generate private key: d (private exponent)
def privateKey_generate(e, totient):
    #return an integer(d) such that e*d mod n = 1

    (a, b, d) = extended_gcd(e, totient)    #calls the extended gcd function
    
    return (a % totient)    #keep public key in ring totient
    
    
#--------------------------------------------------------------------------------------------
#Encryption & Decryption

#   M^e mod n
def encrypt(plaintext, e, n):  
    #(plaintext)^e mod n = ciphertext
    
    #cipher list
    cipher = [] 
    
    #encrypt here
    for x in plaintext:
       temp = ord(x)
       toAppend = pow(temp,e, n) 
       cipher.append(toAppend)
       
    
    temp = []
    for x in cipher:
        temp.append(chr(x))

    #prints the cipher
    print("cipher: ", "".join(temp))    
    print("cipher in integers: ", cipher)
    return cipher


#   C^d mod n
def decrypt(ciphertext, d, n):   
    #(ciphertext)^decryptKey mod n = plaintext
    
    
    #decrypted list
    plain = []
    
    #decrypt here
    for x in ciphertext:
        toAppend = pow(x, d, n) 
        plain.append(chr(toAppend))
        
  
    return plain
    
    
    
#--------------------------------------------------------------------------------------------
#Main Driver

#generate prime numbers
retry = True
while(retry):
    p = getLargePrimeNum()
    q = getLargePrimeNum()
    if(checkPrime(p) and checkPrime(q)):
        retry = False


n = p*q
totient = (p-1)*(q-1)   #phi


find_e = publicKey_generate(totient)
print(str(find_e))

e = 1
d = 1


e = choose_e(find_e)  # (public component) should be greater than 1 but less than (p-1)*(q-1)


#validates for an acceptable private key
while(d <= 1):
    d = privateKey_generate(e, totient)
    print("private key: ",d)
    print("proof: ",(d * e) % totient) # = 1
    if(d <= 1):
        print("private key pair not vaild, please choose another public key: ")
        e = choose_e(find_e)

print("\nPublic Key: (e =", e, ", n =", n,")") 
print("Private Key: ", d, "\n\n")
print("Please wait 3 sec...")
time.sleep(3)


clear = lambda: os.system('clear')
clear()


#password set for the owner account
password = "ironman"
sigVerify = []
info = []
infoPublic = []
check = True




print("\n\nWelcome!\n")


valid = True

#menu inputs and options (I/O)
while(valid):
    print("\n1. Public User\n2. Owner of Keys\n3. Exit Program(Data will not save)")
    user = input("Are you a public user or Owner -(enter number): ")
    if(user == "1"):
        infoPublic = menuPublicUser(e, n, sigVerify)
        if infoPublic:  #keep messages as lists
            infoPublic = split(infoPublic)
    elif(user == "2"):
        while(check):
            passwordCheck = input("\nPlease enter the owner password: ")
            if (passwordCheck == password): #check for password match
                check = False
            else:
                print("Invalid password, retry\n")
                check = True
            
        sigVerify = menuOwner(e, d, n, infoPublic)
        if sigVerify:
            sigVerify = split(sigVerify)
    elif(user == "3"):
        valid = False
    else:
        print("Invalid menu option")
    
exit(0)


