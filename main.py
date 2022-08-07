# RWBSL Duty Scheduler
# Copyright (c) 2022, David Peterson
#
# All rights reserved.

# library import statements
import calendar
import pandas as pd
import sys
import os

# module import statements
from datetime import datetime
import mplcal
import staffMember

# set global variables
# constants
YEAR = datetime.today().year  # current year
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday']  # list of weekdays
WEEKENDS = ['Thursday', 'Friday', 'Saturday']  # list of weekends
NUM_DAYS_YEAR = 365  # number of days in a year

# determine if scheduling for the current month or for the next month
MONTH_SELECT = input("Would you like to schedule for the CURRENT (c) month or the NEXT (n) month? [c/n]: ")
if MONTH_SELECT == 'c':
    MONTH_SELECT_NUM = 0
elif MONTH_SELECT == 'n':
    MONTH_SELECT_NUM = 1
else:
    print("ERROR: Please enter 'c' for the CURRENT month or 'n' for the NEXT month.")
    sys.exit(1)

# set number of staff members on duty and number of sitters weekday/weekend
STAFF_NUM = 3

# month number and string
MONTH_NUM = (datetime.today().month + MONTH_SELECT_NUM) % 12
MONTH_STRING = calendar.month_name[MONTH_NUM]

# number of days in current month
NUM_DAYS_MONTH = calendar.monthrange(datetime.today().year, MONTH_NUM)[1]

# adjust year if scheduling for next-year January in current-year December - special case
if MONTH_SELECT == 'n' and datetime.today().month == 12:
    YEAR += 1

# scheduling dates bounds
SCHEDULE_BOUNDS = input("Would you like to schedule the WHOLE (w) month or PART (p) of the month? [w/p]: ")
if SCHEDULE_BOUNDS == 'w':
    SCHEDULE_START_DAY = 1
    MONTH_END_DAY = NUM_DAYS_MONTH
elif SCHEDULE_BOUNDS == 'p':
    print("Please keep in mind the month of " + MONTH_STRING + " has " + str(NUM_DAYS_MONTH) + " days.")
    SCHEDULE_BOUND_START = input("Please enter the scheduling start date: ")
    SCHEDULE_BOUND_END = input("Please enter the scheduling end date: ")
    if int(SCHEDULE_BOUND_START) < 1 or int(SCHEDULE_BOUND_START) > NUM_DAYS_MONTH or int(SCHEDULE_BOUND_END) < 1 or int(
            SCHEDULE_BOUND_END) > NUM_DAYS_MONTH or SCHEDULE_BOUND_END < SCHEDULE_BOUND_START:
        print("ERROR: Invalid range for scheduling dates.")
        sys.exit(1)
    SCHEDULE_START_DAY = int(SCHEDULE_BOUND_START)
    MONTH_END_DAY = int(SCHEDULE_BOUND_END)
else:
    print("ERROR: Please enter 'w' to schedule the WHOLE month or 'p' to schedule PART of the month.")
    sys.exit(1)

# dictionary to hold names of staff member scheduled for each date
schedule_dict = {}
for i in range(NUM_DAYS_MONTH):
    schedule_dict[i + 1] = ['SM']

# read and create Pandas data frame from Availability XLSX file
BUILDING = input("Input the building/community code (NHW, CHRNE_HARP, etc.): ").upper()
AVAILABILITY_FILE_PATH = "Availability/" + MONTH_STRING + "_" + BUILDING + ".xlsx"
if not os.path.isfile(AVAILABILITY_FILE_PATH):
    print("Incorrect Availability file path. Check that the input file path exists and contains the correct month/building format.")
    print("Format example: monthName_buildingCode.xlsx")
    sys.exit(1)
availability_master = pd.DataFrame(pd.read_excel(AVAILABILITY_FILE_PATH))

# read and create Pandas data frame from History XLSX file
HISTORY_FILE_PATH = "History/" + BUILDING + "_hist.xlsx"
if not os.path.isfile(HISTORY_FILE_PATH):
    print("Incorrect History file path. Check that the input file path exists and contains the correct building format.")
    print("Format example: buildingCode_hist.xlsx")
    sys.exit(1)
history_master = pd.DataFrame(pd.read_excel(HISTORY_FILE_PATH))

# list of staff member names from Availability XLSX file, cumulative weekdays, cumulative weekends
SM_NAMES = availability_master["First Name"].tolist()
SM_CUM_WEEKDAYS = history_master["Weekdays Total"].tolist()
SM_CUM_WEEKENDS = history_master["Weekends Total"].tolist()
SM_CUM_SITTER = history_master["Sitter Total"].tolist()

# list of days the staff members are busy
SM_BUSY_DAYS = availability_master["Days"].tolist()


def main():
    # create staff member object from ResidentAdviser class for each staff member in Availability XLSX file
    SM_DETAILS = {}
    for i in range(len(SM_NAMES)):
        days_ints = []
        days_ints_strings = []
        availability_excel = []
        days_strings = SM_BUSY_DAYS[i]

        # parse Google form output for staff member availability
        if isinstance(days_strings, str):
            days_strings_split = days_strings.split("/")

            for j in range(len(days_strings_split)):
                if j % 2:
                    days_ints_strings.append(days_strings_split[j])

        for k in range(len(days_ints_strings)):
            days_ints.append(int(days_ints_strings[k]))

        for day in range(1, NUM_DAYS_MONTH + 1):
            if day not in days_ints:
                availability_excel.append(day)

        SM_DETAILS[SM_NAMES[i]] = staffMember.StaffMember(SM_NAMES[i], availability_excel, SM_CUM_WEEKDAYS[i], SM_CUM_WEEKENDS[i], SM_CUM_SITTER[1])

    # determine candidates for scheduling on each day of the current month + schedule accordingly based on availability
    for DAY_NUM in range(SCHEDULE_START_DAY - 1, MONTH_END_DAY):
        # candidate selection
        if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
            schedule_current_day(SM_DETAILS, DAY_NUM, True)
        elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
            schedule_current_day(SM_DETAILS, DAY_NUM, False)

    # display schedule summary information
    # confirm correct names scheduled for correct dates
    print("Staff Member Scheduled Dates")
    for keys, SM in schedule_dict.items():
        print(keys, SM)
    print("-------------------------------------------")

    # confirm even distribution of worked day amounts/types
    print("Staff Member Weekday/Weekend Counts")
    for keys, SM in SM_DETAILS.items():
        print(SM.name + " | Weekdays: " + str(SM.scheduled_weekdays) + " | Weekends: " + str(SM.scheduled_weekends) + " | Sitter: " + str(SM.scheduled_sitter))
    print("-------------------------------------------")

    # view staff member availability count for each staff member for the given month
    print("Staff Member Availability")
    for keys, SM in SM_DETAILS.items():
        print(SM.name + " | Availability: " + str(len(SM.availability_clean)) + "/" + str(NUM_DAYS_MONTH) + " days")
    print("-------------------------------------------")

    # create calendar with names of staff members on duty labeled on respective date
    calendar_create = mplcal.MplCalendar(YEAR, MONTH_NUM)
    for DAY_NUM in range(SCHEDULE_START_DAY - 1, MONTH_END_DAY):
        for i in range(STAFF_NUM):
            calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][i])

    # duty schedule review instructions
    print("Once you are done reviewing the duty schedule, please exit out of the calendar pop-up window.")
    input("Press ENTER to view the duty schedule.")
    calendar_create.show()

    # determine if scheduling for the current month or the next month
    user_satisfied = input("Would you like to SAVE (s) the current calendar or EXIT (e) the program [s/e]: ")
    if user_satisfied != 's' and user_satisfied != 'e':
        print("ERROR: Please enter 's' to save the current duty schedule or 'e' to exit the program.")
        sys.exit(1)

    if user_satisfied == 'e':
        print("Exiting the program...")
        sys.exit(1)

    print("Saving calendar and updating History Excel file...")

    # save the calendar image to the corrsponding directory
    calendar_save_path = MONTH_STRING + "_" + str(YEAR) + "_duty_schedule_" + BUILDING
    calendar_create.save("Schedule/" + calendar_save_path)

    # update History XLSX file
    for index, SM in enumerate(SM_DETAILS.values()):
        history_master.loc[index, "Weekdays Total"] = SM.scheduled_weekdays
        history_master.loc[index, "Weekends Total"] = SM.scheduled_weekends
        history_master.loc[index, "Sitter Total"] = SM.scheduled_sitter

    # remove old History XLSX file and save new History XLSX file for future additions
    os.remove(HISTORY_FILE_PATH)
    history_master.to_excel(HISTORY_FILE_PATH, index=False)


def schedule_current_day(SM_DETAILS, DAY_NUM, weekday):
    count_threshold = NUM_DAYS_YEAR
    candidates = []

    for keys, SM in SM_DETAILS.items():
        if weekday:
            CURRENT_DAY_TYPE_SCHEDULED_COUNT = SM.scheduled_weekdays
        else:
            CURRENT_DAY_TYPE_SCHEDULED_COUNT = SM.scheduled_weekends

        if CURRENT_DAY_TYPE_SCHEDULED_COUNT < count_threshold:
            count_threshold = CURRENT_DAY_TYPE_SCHEDULED_COUNT

    while len(candidates) < STAFF_NUM:
        for keys, SM in SM_DETAILS.items():
            if weekday:
                CURRENT_DAY_TYPE_SCHEDULED_COUNT = SM.scheduled_weekdays
            else:
                CURRENT_DAY_TYPE_SCHEDULED_COUNT = SM.scheduled_weekends

            if CURRENT_DAY_TYPE_SCHEDULED_COUNT <= count_threshold and DAY_NUM + 1 in SM.availability_clean and SM.name not in candidates:
                if DAY_NUM:
                    if not (SM.name in schedule_dict[DAY_NUM]):
                        candidates.append(SM.name)
                else:
                    candidates.append(SM.name)

        count_threshold += 1

        if count_threshold == NUM_DAYS_YEAR:
            for key, SM in SM_DETAILS.items():
                print(key, SM.availability_clean)
            print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " - Currently have " + str(len(candidates)) + " candidate(s) | Candidate(s): " + str(candidates))
            sys.exit(1)

    # update day type counts
    for candidate in candidates[0:STAFF_NUM]:
        if weekday:
            SM_DETAILS[candidate].scheduled_weekdays += 1
        else:
            SM_DETAILS[candidate].scheduled_weekends += 1

    # determine sitter index
    sitterIndex = getSitterIndex(SM_DETAILS, candidates[0:STAFF_NUM], DAY_NUM)
    SM_DETAILS[candidates[sitterIndex]].scheduled_sitter += 1

    # append staff member names to the schedule management dictionary
    candidates_selected = []
    for idx, candidate in enumerate(candidates[0:STAFF_NUM]):
        if idx == sitterIndex:
            candidates_selected.append(candidate + " [S]")
        else:
            candidates_selected.append(candidate)

    schedule_dict[DAY_NUM + 1] = candidates_selected


def getSitterIndex(SM_DETAILS, candidates, DAY_NUM):
    count_threshold = NUM_DAYS_YEAR
    sitterIndex = None

    for candidate in candidates:
        CURRENT_SITTER_COUNT = SM_DETAILS[candidate].scheduled_sitter

        if CURRENT_SITTER_COUNT < count_threshold:
            count_threshold = CURRENT_SITTER_COUNT

    while sitterIndex is None:
        for idx, candidate in enumerate(candidates):
            CURRENT_SITTER_COUNT = SM_DETAILS[candidate].scheduled_sitter

            if CURRENT_SITTER_COUNT <= count_threshold and DAY_NUM + 1 in SM_DETAILS[candidate].availability_clean:
                if DAY_NUM > 2:
                    if not (SM_DETAILS[candidate].name in schedule_dict[DAY_NUM]):
                        return idx
                else:
                    return idx

        count_threshold += 1


if __name__ == '__main__':
    main()
