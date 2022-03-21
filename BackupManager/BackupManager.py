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

doDailySync = True
doWeeklyUpdates = True
doMonthlyUpdate = True
doYearlyUpdates = True

#External Directories
syncFile = "D:\Backups\Program\syncFile.txt" #Enter the full directory of where the syncFile is here, The sync file is a file with a list of directories to syncronize before backing up
backupLocation = "D:\Backups"  #Enter the full directory of where backups will be kept

#Number of Backups allowed per type
allowedWeeklyBackups = 4        #Determines max ammount of Weekly Backups
allowedMonthlyBackups = 6       #Determines max ammount of Monthly Backups
allowedYearlyBackups = 99       #Determines max ammount of Yearly Backups

#When backups occur
dateOfWeekly = 0                                    #Defaults as 0, Options: (0-6)
dateOfMonthly = 28                                  #Defaults as 28th, last day of all months(28), Options (1-28)
dateOfYearly = [12, 28]                              #(Month(1-12), Day(1-28))

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
        listID = 0

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

        if not 0 <= dateOfWeekly <= 6:
            print("WARNING: Error detected in the configuration settings.\ndateOfWeekly is not in a valid range, please set the variable between 0-6\n")
            terminationFlag = True
        if not 1 <= dateOfMonthly <= 28:
            print("WARNING: Error detected in the configuration settings.\dateOfMonthly is not in a valid range, please set the variable between 1-28\n")
            terminationFlag = True
        for value in dateOfYearly:
            if listID == 0 and not 1 <= value <= 12:
                print("WARNING: Error detected in the configuration settings.\dateOfYearly (Value 1) is not in a valid range, please set the variable between 1-12\n")
                terminationFlag = True
            if listID == 1 and not 1 <= value <= 28:
                print("WARNING: Error detected in the configuration settings.\dateOfYearly (Value 2) is not in a valid range, please set the variable between 1-28\n")
                terminationFlag = True
            if listID > 2:
                print("WARNING: Error detected in the configuration settings.\dateOfYearly has too many values, please use the format [(Month(1-12), Day(1-28))]\n")
                terminationFlag = True
            listID += 1
        listID = 0
        if terminationFlag: exit()

    #----------------------------------------------------------
    #Function Purpouse: Parses arguments passed from CLI
    #----------------------------------------------------------
    def argParser():
        for arg in sys.argv:
            if arg == "-f":
                backupSys.syncSys()
                backupSys.bakGen("Forced", timeNow.strftime("%m-%d"), "F")
                exit()
            if arg == "-s":
                backupSys.syncSys()
                exit()
            if arg == "-m":
                print("#TODO, manual page")

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
            print("Generating a Sync folder at " + backupLocation + "\n")
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
    #Function Purpouse: Delete old backups after max hit
    #----------------------------------------------------------
    def bacTrimmer(backupType, countedBak):
        deletionFlag = False
        if backupType == "Weekly" and countedBak >= allowedWeeklyBackups:
            deletionFlag = True
        if backupType == "Monthly" and countedBak >= allowedMonthlyBackups:
            deletionFlag = True
        if backupType == "Yearly" and countedBak >= allowedYearlyBackups:
            deletionFlag = True   
        if deletionFlag: dirSorter = sorted(os.listdir(os.curdir)); os.rmdir(dirSorter[0])

    #----------------------------------------------------------
    #Function Purpouse: Dynamicly generate backups
    #----------------------------------------------------------
    def bakGen(backupType, dateCode, backupCode):
        os.chdir(backupLocation)
        if not os.path.isdir(backupType):
            os.mkdir(backupType)
        os.chdir(backupType)
        countedBak = len(next(os.walk(os.curdir))[1])
        backupSys.bacTrimmer(backupType, countedBak)
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
if doWeeklyUpdates and timeNow.weekday() == dateOfWeekly:
    backupSys.bakGen("Weekly", timeNow.strftime("%m-%d"), "W")
if doMonthlyUpdate and timeNow.day == dateOfMonthly:
    backupSys.bakGen("Monthly", timeNow.strftime("%Y-%m"), "M")
if doYearlyUpdates and dateOfYearly == timeNow.strftime("%m-%d"):
    backupSys.bakGen("Yearly", timeNow.strftime("%m-%d"), "Y")

###################################################################################################################################################
#PROGRAM END
###################################################################################################################################################
