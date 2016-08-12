#!/usr/bin/env python
'''
Parser1.2.py: Reads from list file actors.list which can be downloaded from ftp://ftp.fu-berlin.de/pub/misc/movies/database/
this list file contains the IMDB list of actors, and their roles in films and tv-shows. This script parses the actors.list
file into a delimiter file in rows of actorname|TVMovie|roleInMovieOrTV into dFile.txt which can be bulk loaded into sql
'''
# __author__ = 'Ian Johnson'
# _date_ = '8/11/2015'
# _email_ = 'johnson882@gmail.com'

import re
import codecs

list_file = open("actors.list", "r")
aActor = ''
firstName = ''
lastName = ''
thePref = 'I'
# pos = ''
# type = ''
aLine = ''


def bytesInFile(fileName, pieceSize=4096):
    '''
    bytes_from_file() converts input from the inputfile into binary to avoid encoding errors
    Returns:
        b, a character from the input file which is converted to binary
    Args:
        fileName(string): the name of the file being read
        pieceSize(int): buffer size
    '''
    with open(fileName, "rb") as f:
        while True:
            piece = f.read(pieceSize)
            if piece == "":
                break
            for b in piece:
                yield b


print("file Open")
q = re.compile(r'\t+') # regular expression
fOut = codecs.open('dFile.txt', 'w', encoding='utf-8')
newline = "\n"

for b in bytesInFile('actors.list'):
    b = chr(b)
    aLine += str(b)  # converts a row of binary characters into 1 line thats a string

    if "\n" in aLine:  # parses that line into a string
        l = aLine
        aLine = ""
        wList = q.split(l)  # splits line into an list of words

        if len(wList[0]) > 0:
            aActor = wList[0]
            print(aActor)
            tempName = aActor.split(',')

            if len(tempName) > 1:
             firstName = tempName.pop()
             lastName = tempName.pop()


            # print("last name: " + lastName)
             #print("first name: "+ firstName)
             pref = firstName.split('(')
             if len(pref) > 1:
               #thePref = pref.pop()

               thePref = pref[1].strip()

               firstName = pref[0]
              # print("first name: " + firstName)
               thePref = thePref.strip(')')
               print("the Preference:" + thePref)

            if len(tempName) > 0:
                firstName = tempName.pop()
                firstName.strip(' ')
                pref = firstName.split('(')
                #print("pref:" + pref)
                pref = firstName.split('(')
                #print("first name: " + firstName)
                if len(pref) > 1:
                    # thePref = pref.pop()
                    thePref = pref[1].strip()
                    firstName = pref[0]

                    thePref = thePref.strip(')')
                #    print(thePref)
                else:
                    thePref="I"


        if len(wList) > 1:
            print("last name:" + lastName)
            print("first name:" + firstName)
            chrRole = wList[1].split('[')
            firstName = firstName.strip()
            if len(chrRole) > 1:
                tempRole = chrRole[1]
                role = tempRole.split(']')  # pulls out a the character role from the line
                fOut.write(firstName + "|" + lastName  + "|" + thePref + "|" + chrRole[0].strip() + "|" + role[0] + "\r\n")


            if len(chrRole) < 1:
                fOut.write(firstName + "|"+ lastName + "|" + thePref + "|" + chrRole[0].strip() + "|" + "\r\n")
                #print(aActor + "|" + chrRole[0].strip() + "|" + "\r\n")




   # print("line finished")
   # print(firstName)
    #print(lastName)

    if aLine == "Ð":
        break
print("=====================file  created===============================")
fOut.close()
list_file.close()
