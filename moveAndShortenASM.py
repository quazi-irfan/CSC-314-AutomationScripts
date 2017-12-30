
# Automation Script for CSC 314
# Meant to be used with Assignment 7 submissions

# Author : Quazi Irfan; 
# Contact: quazi.irfan@jacks.sdstate.edu

# Program Description:
# This program reads all *.asm files in the current directory. 
# Extracts the student name from the file name, make separate folder for each students and then copy their submission in that folder.
# For example, Given file name "137527-591251 - Jack Hope- Sep 19, 2017 1031 PM - HopeA2.asm"
# 	the program will create a new folder named "Jack Hope" and it will copy the file into that folder.
#	Finally, the program will also rename the file to "HopeA2.asm"
# The program does all of these in 3 passes.

# Tested on Python 3.6.3

import os, shutil, sys

# This section of the code checks if UTIL.LIB and PCMAC.INC is present in the same directory
UTIL_LIB_PATH = os.getcwd() + "\\UTIL.LIB"
PCMAC_INC_PATH = os.getcwd() + "\\PCMAC.INC"
RUN7_PATH = os.getcwd() + "\\run7.bat"

if os.path.isfile(UTIL_LIB_PATH) == False:
    print("Place UTIL.LIB in the same directory with *.ASM files.")
    sys.exit()

if os.path.isfile(PCMAC_INC_PATH) == False:
    print("Place PCMAC.INC in the same directory with *.ASM files.")
    sys.exit()

if os.path.isfile(RUN7_PATH) == False:
    print("Place run7.bat in the same directory with *.ASM files.")
    sys.exit()
    


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
        print("File name does not contain \"AM - \" or \"PM - \" : ", os.getcwd() + "\\" + fileName)
        sys.exit()
    
    return studentName, newFileName




# Pass 1: Check for duplicate;
# This loops assumes, all files from the same students will be found sucessessibely
# For example, if Jack has submitted three files - this loop will loop over Jack's three
#   submission's before moving to Joe's submissions.
duplicate = False
previousStudent = ""
previousStudentsFileList = []
for fileName in os.listdir():
    # Ignore everything but *.asm files
    fileExtension = fileName.split(".")[-1]
    if fileExtension.upper() != 'ASM':
        print("Pass 1: Ignoring ::", fileName)
        continue

    # Extract student, and shortened file name
    studentName, fileName = getStudentNameAndShortenedFileName(fileName)

    # Check if the new file belong to the previous student
    if studentName == previousStudent:
        # If yes, check if the new file already exists in file lists
        if fileName not in previousStudentsFileList:
            previousStudentsFileList.append(fileName)
        else:
            print("PASS 1 DUPLICATE: " + studentName + " has submitted multiple files named " + fileName)
            duplicate = True
    else:
        previousStudent = studentName
        previousStudentsFileList.clear()
        previousStudentsFileList.append(fileName)

# If execution comes to this point, that means...
if duplicate == False:
    print("PASS 1 SUCCESS: No multiple submission with same asm file name from one student detected.")
else:
    print("PASS 1 FAILED: Delete duplicate files, and re-run the script again.")
    sys.exit()




# Pass 2: Access the asm files again and make folders for each students and copy the asm files
for fileName in os.listdir():
    # Ignore everything but *.asm files
    fileExtension = fileName.split(".")[-1]
    if fileExtension.upper() != 'ASM':
        print("Pass 2: IGNORING ::", fileName)
        continue

    # Extract student, and shortened file name
    studentName, fileName_unused = getStudentNameAndShortenedFileName(fileName) #fileName_unused is an unused variable

    # create the folder if it does not already exists
    if not os.path.exists(studentName):
        os.makedirs(studentName)

    # copy the file to that folder
    sourcePath = os.path.abspath(fileName) 
    destinationPath = os.getcwd() + "\\" + studentName
    shutil.move(sourcePath, destinationPath)

print("PASS 2 SUCCESS: Sucessfully created folder per student, and copied UTIL.LIB, PCMAC.INC and run7.bat")





## Pass 3: Go in each folder to rename(shorten) the long asm file names
for folderName in os.listdir():

    # Since os.listdir() fetchs both files and folder, we need to skip files
    if os.path.isfile(os.path.abspath(folderName)):
        print("PASS 3: IGNORING :: ", folderName)
        continue    

    # Go inside the folder
    os.chdir(os.getcwd() + "\\" + folderName)  

    # Rename each file
    for fileName in os.listdir():
        # Ignore everything but *.asm files
        fileExtension = fileName.split(".")[-1]
        if fileExtension.upper() != 'ASM':
            print("Pass 2: IGNORING ::", fileName)
            continue

        studentName, shortenedFileName = getStudentNameAndShortenedFileName(fileName)
        
        # Rename        
        sourceFile = os.path.abspath(fileName)
        destinationFile = os.getcwd() + "\\" + shortenedFileName
        shutil.move(sourceFile, destinationFile)

        # Copies UTIL.LIB and PCMAC.INC with the asm file
        shutil.copyfile(UTIL_LIB_PATH, os.getcwd()+ "\\UTIL.LIB")
        shutil.copyfile(PCMAC_INC_PATH, os.getcwd()+ "\\PCMAC.INC")
        shutil.copyfile(RUN7_PATH, os.getcwd()+ "\\run7.bat")

    # Come out of that folder so our loop can move to the next folder
    os.chdir("../")

print("PASS 3 SUCCESS: Sucessfully renamed(shortened) all asm file names.")

    
