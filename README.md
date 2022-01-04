# Automated RA Duty Scheduler
Create an RA Duty Schedule in seconds!

**Author:** David Peterson - dpeterson23@vt.edu

**Version:** V1. 01-04-2022

V1.1 - Partnerships Added - program prioritizes matching you with new RAs

V1.2 - Custom number of staff for weekdays/weekends

V1.3 - History Added - automatically import cumulative number of worked weekdays/weekends

V1.4 - Enhanced user input procedures, automatic refreshing calendar, ensure at least 5 days between scheduled days

If you experience any bugs/errors or would like to suggest an improvement, please contact me by emailing dpeterson23@vt.edu

# How to Use
1) Download and Set-Up PyCharm (Free)
2) Create your Availability Excel file and History Excel in the correct format
3) Save the Availability Excel file in the correct location and run the program once a month
4) View your automatically created duty schedule in a calendar like this!

![](images/calendar.png)


## PyCharm Set-Up
You only have to do these steps for a first-time set-up. The steps below are very specific, if you have any trouble please reference this site for detailed instructions for set-up procedures with PyCharm (compatible with Windows and Mac): https://www.jetbrains.com/help/pycharm/quick-start-guide.html

If you have persistent trouble setting this up, feel free to email me and I am happy to help!

**Install Python/PyCharm IDE**
1) If you do not have a version of Python installed on your computer, download it here: https://www.python.org/downloads/
1) Go here: https://www.jetbrains.com/pycharm/download/ and download the PyCharm Community Edition (Free)
3) Once PyCharm is downloaded, go here: https://github.com/dpetersonVT23/RA_Duty_Scheduler
4) Click on the green "Code" button, it will drop down with an "HTTPS" link, click the clipboard to copy this link (it will confirm you copied it)
5) Open PyCharm, click "Get from Version Control" or "Get from VCS", paste the "HTTPS" link you just copied in the URL box
6) Set the directory on your computer in a location you know how to access in the Directory box
7) Click the "Clone" button

**Set-Up Python Interpreter**
1) Navigate to Settings (Windows)/Preferences (Mac), and click the dropdown menu next to "Project: RA_Duty_Scheduler"
2) Click on Python Interpreter
3) Click the gear icon in the upper-right => Add... => Virtualenv Environment => New Environment
4) Click the dropdown menu to select your "Base Interpreter" and select the option that corresponds with Python 3 (might appear as /usr/bin/python3)
5) Click OK and let it load, you should see "pip" and "setuptools" under packages, you are now ready to install the necessary packages for the program

**Installing Packages**

This program needs support from external libraries to function correctly, once your Python Interpreter is set-up, you can install these packages to ensure everything works correctly for you.

Click the + sign to install additional packages. Please search for and install the following packages:
- pandas
- matplotlib
- openpyxl

**Set-Up Python Configuration**

This is the last step, you are almost done with this one-time set-up!

1) On the main screen of the IDE (Integrated Development Environment), click "Add Configuration..." on the top
2) Click the + sign in the upper-left and click "Python"
3) You need to set 2 things under the Configuration menu: Script Path + Python Interpreter
4) Set the script path to main.py - locate where you put the "RA_Duty_Scheduler" program by clicking the folder icon, click main.py, and click open
5) Set the Python Interpreter to the Interpreter you just made - the one you want to select will most likely have "RA_Duty_Scheduler" in parentheses () with Python 3.X next to it
6) Click OK and you're Python environment is all ready to go!

## Running the Program
Create a Google form that allows residents to choose which dates they are **not** available. Please see this example form for August (credit Illa Rochez): https://forms.gle/tvbEhKGmkEREgkdB7 - You will see a section to mark days UNAVAILABLE and NOT IDEAL, the program only uses days an RA is UNAVAILABLE to schedule. Use dates for NOT IDEAL to find backup RAs if you don't have enough RAs on a given day.

Please ensure the options for selecting when an RA is busy is formatted as "DAY: MONTH/DAY/YEAR". (e.g., Sunday: 08/15/2021)

You will be able to export data from the Google form responses to be used as the Availability Excel file for the program. This is what the output file might look like, however, there are some things you want to make sure of before inputting it to the program.

![](images/excel_1.png)

1) Ensure the column header for the RA Names is "First Name"
2) Ensure the column header for the days the RA is not available is "Days"
3) Ensure the name of the Availability Excel file is "monthName_buildingCommunityCode.xlsx" - (The building code is ultimately up to you, just remember how you name the file for when you run the program as you will be prompted for the building code in the terminal - see existing examples in the Availability directory - ensure the month name is LOWERCASE and the building/community code is UPPERCASE)

Locate where in your file explorer you set-up the Python program when you clicked "Get from Version Control" or "Get from VCS". Open the RA_Duty_Scheduler folder. Here you will see an Availability folder and a History folder, this is where you will place your excel files that manage availability for RAs and cumulative weekdays/weekends worked.

Save the availability Excel file here. Now it is time to set up the History Excel file. The purpose of this file is to automatically track how many weekdays/weekends each RA on your staff works so that it can be most accurately balanced over the course of the semester. Please reference the image below to set-up your History Excel file (you only have to do this once as this file updates automatically every time the program is run). If you are starting mid-semester with this program, instead of filling in both columns with all zeros, you can fill in the current amount of weekdays/weekends worked for each of your staff so the program can best balance duty scheduling for your staff for the remainder of the semester. Please name the column headers exactly how they appear in the image below for the program to work correctly. Also, please ensure the name of the History Excel file is "buildingCommunityCode_hist.xlsx", where the building/community code is UPPERCASE. If you ever want to automatically reset this history, use the prompt at the end of the script to do so - you will be prompted to reset it in the terminal (you cannot undo this action). Feel free to save copies of this History Excel file for your own records in case you write over the original and can't get the data back.

![](images/excel_2.png)

Now to run the program! Click the Green Play button, fill in the prompts in the terminal accordingly, and your Calendar will pop-up and automatically be saved to the Schedule folder for you to access and share with your RAs! In addition, your History Excel file will be updated with a running sum of worked weekdays/weekends automatically and will use these values to appropiately assign a balanced duty schedule over the course of the semester.

**IMPORTANT NOTE:** Once the calendar pops up, hit the X in the upper corner and close the window so that the program continues and saves your History Excel file. Do not worry as your calendar will automatically be saved in the Schedule directory.

**Run Output:** In the "Run" tab, at the bottom of the PyCharm IDE, you will see a series of outputs after you run the program providing you additional information about your newly generated RA Duty Calendar. From top to bottom, you will find a list of the RAs on duty each day (RAs Scheduled Dates), the cumulative number of weekdays/weekends each RA has been scheduled at that point in the semester (RA Weekday/Weekend Counts), the number of unique RAs each RA is partnered up with on duty (along with who specifically these unique RAs are) (RA Partnerships), and the number of days the RA submitted that they were available for a given month (RA Availability)!

# Advanced Tips

## Checking for Updates
It is smart to check for any updates (improvements) made to the code before you run the program to schedule RA duty for the month. To check for any updates, locate the Diagonal Blue Arrow located in the upper-right corner of the PyCharm IDE. When you hover over this arrow it will say "Update Project...". Click on the arrow icon, select OK, and your program will check for updates (automatically updating as necessary). A small pop-up will appear in the lower-right corner of the screen confirming once the program has finishing updating.

## Not Enough Candidates Warning
If you get a warning that looks like this in the "Run" tab at the bottom of the PyCharm IDE, this means there are not enough RAs available for duty on the specified day. A warning like this may appear as the following:

NOT ENOUGH CANDIDATES FOR JULY 22 (WEEKDAY) - Currently have 1 candidate(s) | Candidates: [nameOfCurrentCandidates]

This means that on July 22nd, only 1 of your RAs has noted that they are available for duty but you might need atleast 2 to be available. Reach out and find someone else who is willing to fill in and be the second RA on duty for that day!
