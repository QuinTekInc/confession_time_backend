
import string 
import random

ALL_LETTERS = string.printable #comprise of all characters in the form: digits + lowercase + uppercase + symbols + whitespace
ALL_LETTER_LENGTH: int = len(ALL_LETTERS)

def encryptStr(word: str) -> str:
    
    enc: str = ''

    for character in word:

        if character not in ALL_LETTERS:
            enc += character
            continue
       
        enc += ALL_LETTERS[(ALL_LETTERS.index(character) + 5) % ALL_LETTER_LENGTH] 

        pass 

    return enc


def decryptStr(encryptedWord: str):

    dec: str = ''

    for character in encryptedWord:

        if character not in ALL_LETTERS:
            dec += character 
            continue 

        dec += ALL_LETTERS[(ALL_LETTERS.index(character) - 5) % ALL_LETTER_LENGTH]

    
    return dec


def leadingZeros(number: int) -> str:

    zeros: str = ''

    while len(zeros) + len(str(number)) != 3:
       zeros += '0'

    return f'{zeros}{number}'


 
def generateRandomNumber() -> str:

    #first three numbers
    first_three_numbers = leadingZeros(random.randint(0, 1000))

    #second three numbers
    second_three_numbers = leadingZeros(random.randint(0, 1000))

    return f'{first_three_numbers}-{second_three_numbers}'


def detailFormat(message:str) -> dict:
    return {'detail': message}