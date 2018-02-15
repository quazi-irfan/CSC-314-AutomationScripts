
# Automation Script for CSC 314
# Meant to be used with Assignment 1-6, 8 submissions

# Author : Quazi Irfan; 
# Contact: quazi.irfan@jacks.sdstate.edu

# Program Description:
# This program reads all *.asm files in the current directory and shortens them.
# For example, Given file name "137527-591251 - Jack Hope- Sep 19, 2017 1031 PM - HopeA2.asm"
# 	the program will remove the first part of the file name, and rename the file to "HopeA2.asm"
# Because there might be another file with the same name, the program work check if there will be any collision in Pass 1.
# Actual rename takes place in Pass 2.

# Tested on Python 3.6.3

import os
import shutil
import sys

# This function takes a long file name, and extracts and returns the student name and the shortened file name
# For example, Given file name "137527-591251 - Jack Hope- Sep 19, 2017 1031 PM - HopeA2.asm"
#   the function will return two strings, "Jack Hope" and "HopeA2.asm"
def getStudentNameAndShortenedFileName(fileName):
    index1 = fileName.find('-') +1                  # locate the first occurance of '-' character      
    index2 = fileName.find('-', index1 + 1) + 2     # find the second occurance of '-' character
    index3 = fileName.find('-', index2)             # find the third occurance of '-' character 
    studentName = fileName[index2:index3]           # use the second and third occurange to extract student name

    if fileName.find("AM - ") != -1 or fileName.find("PM - ") != -1:
        # Extract file name
        reverseFileName = fileName[::-1]        
        endIndex = 0;
        if reverseFileName.find(" - MA") != -1:
            endIndex = reverseFileName.find(" - MA")
        elif reverseFileName.find(" - MP") != -1:
            endIndex = reverseFileName.find(" - MP")

        newReversedFileName = reverseFileName[:endIndex]
        newFileName = newReversedFileName[::-1]
        
    else:
        print("File name does not contain \" - AM\" or \" - PM\" : ", fileName)
        sys.exit()
    
    return studentName, newFileName




## Pass 1: Check for duplication, Only *.asm files
duplicate = False
listOfShortenedFileNames = []
for fileName in os.listdir():
    fileExtension = fileName.split(".")[-1]
    if fileExtension.upper() != 'ASM':
        print("Pass 1: IGNORING ::", fileName)
        continue
    
    studentName_unused, shortenedFileName = getStudentNameAndShortenedFileName(fileName)

    ## append the file name to a list to check back later
    if shortenedFileName not in listOfShortenedFileNames:
        listOfShortenedFileNames.append(shortenedFileName)            
    else:
        print("PASS 1 DUPLICATE: File name Collision ::", fileName , ". Deleted older versions of", shortenedFileName)
        duplicate = True

if duplicate == False:
    print("PASS 1 SUCCESS: Shortening all files won't result in file name collision.")
else:
    print("PASS 1 FAILED: Delete duplicate files, and re-run the script again.")
    sys.exit()



## Pass 2: Rename all files
for fileName in os.listdir():
    fileExtension = fileName.split(".")[-1]
    if fileExtension.upper() != 'ASM':
        print("Pass 2: IGNORING ::", fileName)
        continue

    studentName_unused, shortenedFileName = getStudentNameAndShortenedFileName(fileName)

    ## rename the file
    source = os.path.abspath(fileName)
    destination = os.getcwd() + "\\" + shortenedFileName
    shutil.move(source, destination) 

print("PASS 2 SUCCESS: Shortened all *.asm file.")
    
    
