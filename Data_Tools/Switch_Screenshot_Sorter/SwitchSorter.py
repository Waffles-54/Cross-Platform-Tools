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

class dataInit:
    #----------------------------------------------------------
    #Function Purpouse: Gets and validates the location of the switches screenshots from the user
    #----------------------------------------------------------
    def getSwitchScreenies():
        validPath = False
        pathGiven = ''

        while(not validPath):
            print("Please enter the full directory of where your Nintendo Screenshots are located: ")
            pathGiven = input()
            validPath = os.path.exists(pathGiven)

        return pathGiven

    def initOrginizedStructure(pathGiven):
        os.chdir(pathGiven)
        if not os.path.exists("Sorted Screenshots"):
            print("Generating Sorted Screenshots folder at " + pathGiven)
            os.mkdir("Sorted Screenshots")
        
        os.chdir("Sorted Screenshots")
        return os.getcwd()


#####################################################################
#ENTRY POINT
#####################################################################

import os, shutil

ScreeniesLocale = dataInit.getSwitchScreenies()
OrginizedScreenies = dataInit.initOrginizedStructure(ScreeniesLocale)

for root, directories, files in os.walk(ScreeniesLocale):
	for data in files:
            #ID Proccessing
            gameID = data.split('-')
            gameID = gameID[1].split('.')
            gameID = gameID[0]

            os.chdir(OrginizedScreenies)
            if not os.path.exists(gameID):
                os.mkdir(gameID)
            originalFile = os.path.join(root, data)
            newFile = os.path.join(OrginizedScreenies, gameID, data)
            shutil.move(originalFile, newFile)

print("Screenshots have been orginized.")

##########################################################################################################################
#PROGRAM END
###################################################################################################################################################