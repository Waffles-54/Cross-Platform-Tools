# Backup Manager
A system for maintaining backups
## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General Info
This project serves as a backup management system with configurable settings to fine tune how you want your backups done. It is designed to work on any system and has built in fail checking.

## Technologies
- [Python 3.10.2](https://www.python.org/)
- [dirsync](https://pypi.org/project/dirsync/)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [tarfile](https://docs.python.org/3.8/library/tarfile.html)

## Setup
### Downloading
#### CLI
- cd directory_of_install
- git clone https://github.com/WaffleGod54/Cross-Platform-Tools
### Configuration
#### Breakdown
- Toggles: Controls what kinds of backups the system makes
  - doDailySync: Determines if the system will syncronize folders to a location before backing up
  - doWeeklyBackups: Determines if backups are generated on a weekly basis
  - doMonthlyBackups: Determines if backups are generated on a monthly basis
  - doYearlyBackups:  Determines if backups are generated on a yearly basis
- External Directories: Controls where the system pulls directories from
  - syncFile: If doDailySync is enabled, the system requires the full directory of a file with a list of directories to syncronize before backing up
  - backupFile: the backupFile is a file with a list of directories that tells the system what to backup (for directories not included in the syncFile)
  - backupLocation: This directory tells the system where to generate backups (including syncronization)
- Number of Backups allowed per type: Controls the max ammount of backups that can be kept on a system
  - allowedWeeklyBackups: This value is the max allowed of weekly updates that are maintained by the system
  - allowedMonthlyBackups: This value is the max allowed of monthly updates that are maintained by the system
  - allowedYearlyBackups: This value is the max allowed of yearly updates that are maintained by the system
- When Backups occur: Controls the dates of when backups are created
  - dateOfWeekly: this value (0-6) determines what day to take weekly backups
  - dateOfMonthly: this value (1-28) determines what day to take monthly backups
  - dateOfYearly: these values (1-12, 1-28) determines what day to take yearly backups
#### CLI
I reccomend using the nano editor:
- cd BackupManager
- nano BackupManager.py
Edit the configuration to make the system opperate how you like
### Automation
#### Linux
- crontab -e
- 30 * * * * /directory/of/BackupManager.py
- Ctrl + O
- Enter
- Ctrl + X
