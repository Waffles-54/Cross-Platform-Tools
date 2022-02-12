###################################################################################################################################################
#Written By Keegan A Clark, Everett Community College
#Initial Commit: 2021.11.25, Last Edited: 2022.02.11
#This program is licensed under the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl-3.0.en.html
#This program is not under any form of warranty
#Purpouse Statement:
#This program is designed to be the configurable program for backing up systems on any platform
###################################################################################################################################################

###################################################################################################################################################
#CONFIGURATION
###################################################################################################################################################
doDailySync = True
doWeeklyUpdates = True
doMonthlyUpdate = True
doQuarterlyUpdates = True
doBiannualUpdates = True
doYearlyUpdates = True

#External Directories
syncFile = "/mnt/bak/syncFile.txt" #Enter the full directory of where the syncFile is here, The sync file is a file with a list of directories to syncronize before backing up
backupLocation = "/mnt/bak"  #Enter the full directory of where backups will be kept

#Number of Backups allowed per type (NOT YET IMPLEMENTED) #TODO
# allowedWeeklyBackups = 4        #Determines max ammount of Weekly Backups
# allowedMonthlyBackups = 3       #Determines max ammount of Monthly Backups
# allowedQuarterlyBackups = 4     #Determines max ammount of Quarterly Backups
# allowedBiannualBackups = 2      #Determines max ammount of Biannual Backups
# allowedYearlyBackups = 99       #Determines max ammount of Yearly Backups

#When backups occur
dateOfWeekly = 0                                    #Defaults as 0, Options: (0-6)
dateOfMonthly = 28                                  #Defaults as 28th, last day of all months(28), Options (1-31)
dateOfQuarterly = ["03-28","06-28","09-28","12-28"] #(Month(1-12)-Day(1-31))
dateOfBiannual = ["06-28" ,"12-28"]                 #(Month(1-12)-Day(1-31))
dateOfYearly = "12-31"                              #(Month(1-12)-Day(1-31))

#General 
#!/usr/bin/python
import os, sys, datetime, dirsync, tarfile
timeNow = datetime.datetime.today()

###################################################################################################################################################
#END OF CONFIGURATION
###################################################################################################################################################

###################################################################################################################################################
#PROGRAM START
###################################################################################################################################################

#####################################################################
#Class Purpouse: Preparing the program to opperate
#####################################################################
class prepSystem:
    #Method to validate the configuration settings are correct
    def validateConfiguration():
        terminationFlag = False
        #Validates the flags on types of updates
        if not type(doDailySync) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoDailySync must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doWeeklyUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoWeeklyUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doMonthlyUpdate) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoMonthlyUpdate must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doQuarterlyUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoQuarterlyUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doBiannualUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoBiannualUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        if not type(doYearlyUpdates) == bool:
            print("WARNING: Error detected in the configuration settings.\ndoYearlyUpdates must be a bool (True or False)\nCaps are important, make sure the value is capitalized\n")
            terminationFlag = True
        
        #Validates the paths that the O.S needs to access later
        if not os.path.exists(backupLocation):
            print("WARNING: Error detected in the configuration settings.\nbackupLocation was unable to be located, Please validate the path\n")
            terminationFlag = True
        if not os.path.isfile(syncFile) and doDailySync:
            print("WARNING: Error detected in the configuration settings.\nsyncFile was unable to be opened, Please validate the path\n")
            terminationFlag = True

        #Validates the times to take backups
        if 0 <= dateOfWeekly <= 6:
            print("WARNING: Error detected in the configuration settings.\ndateOfWeekly must be between 0 and 6\n")
            terminationFlag = True
        if 1 <= dateOfMonthly <= 31:
            print("WARNING: Error detected in the configuration settings.\ndateOfMonthly must be between 1 and 31\n")
            terminationFlag = True
        # for each in dateOfQuarterly:
            #[mm-dd]
            #[(int)(int)-(int)(int)]
            #[mm][dd]
            #[mm] 1 - 12
            #[dd] 1 - 31
        # for each in dateOfBiannual:
        #     print("Placeholder")
        # for each in dateOfYearly:
        #     print("Placeholder")

        if terminationFlag: exit()

    #Method to parse arguments passed into the program via command line
    def argumentParser():
        for each in sys.argv:
            if "-F" == each == "-f":
                backupTypes.generateBackup("Forced", timeNow.strftime("%d"), "F")
                exit()
            else:
                print(each + " is not a recognized paramater")


#####################################################################
#Class Purpouse: Backup functionality
#####################################################################

class backupTypes:
    #Method to sync system
    def syncBackups():
            os.chdir(backupLocation)
            if not os.path.isdir("Sync"):
                print("Generating a Sync folder at " + backupLocation)
                os.mkdir("Sync")
            os.chdir("Sync")
            with open(syncFile) as sync:
                for line in sync:
                    currSync = os.path.basename(line).strip('\n')
                    if not currSync == '':
                        if not os.path.isdir(currSync): 
                            os.mkdir(currSync)
                        print("Sycronizing " + currSync + "...")
                        dirsync.sync(line.strip('\n'), currSync, 'sync')

    #Method to generate backups
    def generateBackup(backupType, dateCode, backupCode):
        os.chdir(backupLocation)
        if not os.path.isdir(backupType):
            os.mkdir(backupType)
        os.chdir(backupType)
        if not os.path.isdir(dateCode):
            os.mkdir(dateCode)
        os.chdir(dateCode)
        bakLoc = os.getcwd()
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
                    os.chdir(syncLoc)                                       #Change directory to the Sync location for the next cycle

###################################################################################################################################################
#PROGRAM END
###################################################################################################################################################

###################################################################################################################################################
#ENTRY POINT
###################################################################################################################################################

prepSystem.argumentParser()
prepSystem.validateConfiguration()

if doDailySync:
    backupTypes.syncBackups()

if doWeeklyUpdates and timeNow.weekday() == dateOfWeekly:
    backupTypes.generateBackup("Weekly", timeNow.strftime("%m-%d"), "W")

if doMonthlyUpdate and timeNow.day == dateOfMonthly:
    backupTypes.generateBackup("Monthly", timeNow.strftime("%Y-%m"), "M")

if doQuarterlyUpdates:
    for timeCode in dateOfQuarterly:
        if timeNow.strftime("%m-%d") == timeCode:
            backupTypes.generateBackup("Quarterly", timeNow.strftime("%m-%d"), "Q")

if doBiannualUpdates:
    for timeCode in dateOfBiannual:
        if timeNow.strftime("%m-%d") == timeCode:
            backupTypes.generateBackup("Biannual", timeNow.strftime("%m-%d"), "B")

if doYearlyUpdates and dateOfYearly == timeNow.strftime("%m-%d"):
    backupTypes.generateBackup("Yearly", timeNow.strftime("%m-%d"), "Y")

###################################################################################################################################################
#END OF APPLICATION
###################################################################################################################################################