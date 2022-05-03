###################################################################################################################################################
#Written By Keegan A Clark, Washington State University
#Initial Commit: 
#This program is licensed under the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl-3.0.en.html
#This program is not under any form of warranty
#Purpouse Statement:
#A program to sort switch screenshots in a more reasonable way
###################################################################################################################################################

###################################################################################################################################################
#PROGRAM START
###################################################################################################################################################
import os, shutil

currentDir = os.path.join(os.getcwd(), "Album")
if not os.path.isdir(currentDir):
    print("The Album folder was not detected, place this program in the Nintendo root folder")
    exit()
if not os.path.exists("Sorted Screenshots"):
            print("Generating Sorted Screenshots folder...")
            os.mkdir("Sorted Screenshots")   
os.chdir("Sorted Screenshots")
sortedData = os.getcwd()
for root, directories, files in os.walk(currentDir):
	for data in files:
            #ID Proccessing
            gameID = data.split('-')
            gameID = gameID[1].split('.')
            gameID = gameID[0]

            os.chdir(sortedData)
            if not os.path.exists(gameID):
                os.mkdir(gameID)
            originalFile = os.path.join(root, data)
            newFile = os.path.join(os.getcwd(), gameID, data)
            shutil.move(originalFile, newFile)

shutil.rmtree(currentDir)
print("Screenshots have been orginized.")

###################################################################################################################################################
#PROGRAM END
###################################################################################################################################################