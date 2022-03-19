###################################################################################################################################################
#Written By Keegan A Clark, Western Washington University
#Initial Commit: 2021.11.25, Last Edited: 2022.02.11
#This program is licensed under the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl-3.0.en.html
#This program is not under any form of warranty
#Purpouse Statement:
#This program is designed to be the configurable program for backing up systems on any platform
###################################################################################################################################################

#!/usr/bin/python
import os, sys, subprocess

###################################################################################################################################################
#CONFIGURATION START
###################################################################################################################################################

doDailySync = False
doWeeklyUpdates = True
doMonthlyUpdate = True
doYearlyUpdates = True

#External Directories
syncFile = "D:\Backups\Program\syncFile.txt" #Enter the full directory of where the syncFile is here, The sync file is a file with a list of directories to syncronize before backing up
backupLocation = "D:\Backups"  #Enter the full directory of where backups will be kept

#Number of Backups allowed per type (NOT YET IMPLEMENTED) #TODO
# allowedWeeklyBackups = 4        #Determines max ammount of Weekly Backups
# allowedMonthlyBackups = 3       #Determines max ammount of Monthly Backups
# allowedQuarterlyBackups = 4     #Determines max ammount of Quarterly Backups
# allowedBiannualBackups = 2      #Determines max ammount of Biannual Backups
# allowedYearlyBackups = 99       #Determines max ammount of Yearly Backups

#When backups occur
dateOfWeekly = 0                                    #Defaults as 0, Options: (0-6)
dateOfMonthly = 28                                  #Defaults as 28th, last day of all months(28), Options (1-31)
dateOfYearly = [12, 31]                              #(Month(1-12), Day(1-31))

###################################################################################################################################################
#CONFIGURATION END 
###################################################################################################################################################

###################################################################################################################################################
#PROGRAM START
###################################################################################################################################################

#####################################################################
#Class Purpouse: Preparing the program to opperate
#####################################################################

class prepSys:
    #----------------------------------------------------------
    #Function Purpouse: Checks for required package installs
    #----------------------------------------------------------
    def preReq():
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dirsync'])

    #----------------------------------------------------------
    #Function Purpouse: Checks that configuration is good
    #----------------------------------------------------------
    def ConfCheck():
        terminationFlag = False

        #BOOL CHECKING PHASE
        if not type(doDailySync) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoDailySync must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doWeeklyUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoWeeklyUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doMonthlyUpdate) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoMonthlyUpdate must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doYearlyUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoYearlyUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True

        #PATH & FILE CHECKING PHASE
        if not os.path.exists(backupLocation):
            print("WARNING: Error detected in the configuration settings.\nbackupLocation was unable to be located, Please validate the path\n")
            terminationFlag = True
        if not os.path.isfile(syncFile) and doDailySync:
            print("WARNING: Error detected in the configuration settings.\nsyncFile was unable to be opened, Please validate the path\n")
            terminationFlag = True

        if terminationFlag: exit()

        #DATECODE CHECKING
        #TODO

    #----------------------------------------------------------
    #Function Purpouse: Parses arguments passed from CLI
    #----------------------------------------------------------
    def argParser():
        for each in sys.argv:
            if each == "-f":
                backupSys.syncSys()
                backupSys.bakGen("Forced", timeNow.strftime("%m-%d"), "F")
                exit()
            if each == "-s":
                backupSys.syncSys()
                exit()
                

#####################################################################
#Class Purpouse: Program functionality
#####################################################################
class backupSys:
    #----------------------------------------------------------
    #Function Purpouse: Syncronize the backup system
    #----------------------------------------------------------
    def syncSys():
        os.chdir(backupLocation)
        if not os.path.isdir("Sync"):
            print("Generating a Sync folder at " + backupLocation)
            os.mkdir("Sync")
        os.chdir("Sync")
        with open(syncFile) as sync:
            for line in sync:
                #TODO: KNOWN BUG: os.path.basename strips everything if just a drive letter
                currSync = os.path.basename(line).strip('\n')
                if not currSync == '':
                    if not os.path.isdir(currSync): 
                        os.mkdir(currSync)
                    print("Sycronizing " + currSync + "...")
                    dirsync.sync(line.strip('\n'), currSync, 'sync')
    
    #----------------------------------------------------------
    #Function Purpouse: Dynamicly generate backups
    #----------------------------------------------------------
    def bakGen(backupType, dateCode, backupCode):
        os.chdir(backupLocation)
        if not os.path.isdir(backupType):
            os.mkdir(backupType)
        os.chdir(backupType)
        if not os.path.isdir(dateCode):
            os.mkdir(dateCode)
        os.chdir(dateCode)
        bakLoc = os.getcwd()
        #TODO: BUG: Remove the requirment of the Sync Folder and make it a dynamic location of where to generate from
        os.chdir(backupLocation)
        os.chdir("Sync")
        syncLoc = os.getcwd()
        for subdir, dirs, files in os.walk(syncLoc):                        #For each directory in the Sync folder,
                for dir in dirs:                                            #Needed repeat to isolate directories
                    os.chdir(dir)                                           #Change directory into the current Synced Folder
                    addFile = os.getcwd()                                   #Sets up location of what to backup
                    os.chdir(bakLoc)                                        #Change directory to the Backup Location
                    tarName = backupCode + "-" + dir + ".tar.gz"            #Setup tarfile name
                    print("Backing up " + dir + " to " + bakLoc + "...")    #Diagnostcis & Reporting
                    newTar = tarfile.open(tarName,'w:gz')                   #Generate a new tarfile for the 
                    newTar.add(addFile)                                     #Add files to the archive
                    print(dir + " has been sucsessfully backed up.")        #Diagnostcis & Reporting
                    newTar.close()                                          #Close the archive
                    os.chdir(syncLoc)  
    
#####################################################################
#ENTRY POINT
#####################################################################

#Prep Phase
prepSys.preReq()
prepSys.ConfCheck()
import tarfile, datetime, dirsync
timeNow = datetime.datetime.today()

#Program Phase
prepSys.argParser()
if doDailySync:
    backupSys.syncSys()

if doWeeklyUpdates:# and timeNow.weekday() == dateOfWeekly:
    backupSys.bakGen("Weekly", timeNow.strftime("%m-%d"), "W")

if doMonthlyUpdate and timeNow.day == dateOfMonthly:
    backupSys.bakGen("Monthly", timeNow.strftime("%Y-%m"), "M")

if doYearlyUpdates and dateOfYearly == timeNow.strftime("%m-%d"):
    backupSys.bakGen("Yearly", timeNow.strftime("%m-%d"), "Y")

###################################################################################################################################################
#PROGRAM END
###################################################################################################################################################
