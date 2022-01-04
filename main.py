# RA Duty Scheduler
# Copyright (c) 2021, David Peterson
#
# All rights reserved.

# library import statements
import calendar
import pandas as pd
import sys
import random
import os

# module import statements
from datetime import datetime
from RA import ResidentAdviser
from mplcal import MplCalendar

# set global variables
# constants
YEAR = datetime.today().year  # current year
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']  # list of weekdays
WEEKENDS = ['Friday', 'Saturday']  # list of weekends
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

# set number of RAs on duty weekday/weekend
WEEKDAY_STAFF_NUM = int(input("How many RAs would you like scheduled on weekdays (Sun-Thurs)? (between 0 and 3): "))
WEEKEND_STAFF_NUM = int(input("How many RAs would you like scheduled on weekends (Fri-Sat)? (between 0 and 3): "))
if not (0 <= WEEKDAY_STAFF_NUM <= 3) or not (0 <= WEEKEND_STAFF_NUM <= 3):
    print("ERROR: Program only schedules between 0 and 3 RAs for weekdays/weekends.")
    sys.exit(1)

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

# dictionary to hold names of RA scheduled for each date
schedule_dict = {}
for i in range(NUM_DAYS_MONTH):
    schedule_dict[i + 1] = ['RA']

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

# list of RA names from Availability XLSX file, cumulative weekdays, cumulative weekends, cumulative partnerships
RA_NAMES = availability_master["First Name"].tolist()
RA_CUM_WEEKDAYS = history_master["Weekdays Total"].tolist()
RA_CUM_WEEKENDS = history_master["Weekends Total"].tolist()

# list of days the RA's are busy
RA_BUSY_DAYS = availability_master["Days"].tolist()


def main():
    # while the user is not satisfied with the duty schedule, create new versions
    user_satisfied = 'n'

    while user_satisfied == 'n':
        # create RA object from ResidentAdviser class for each RA in Availability XLSX file
        RA_DETAILS = {}
        for i in range(len(RA_NAMES)):
            days_ints = []
            days_ints_strings = []
            availability_excel = []
            days_strings = RA_BUSY_DAYS[i]

            # parse Google form output for RA availability
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

            RA_DETAILS[RA_NAMES[i]] = ResidentAdviser(RA_NAMES[i], availability_excel, RA_CUM_WEEKDAYS[i], RA_CUM_WEEKENDS[i])

        # determine candidates for scheduling on each day of the current month + schedule accordingly based on availability
        for DAY_NUM in range(SCHEDULE_START_DAY - 1, MONTH_END_DAY):
            # candidate selection
            if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
                schedule_current_day(RA_DETAILS, DAY_NUM, True)
            elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
                schedule_current_day(RA_DETAILS, DAY_NUM, False)

        # display schedule summary information
        # confirm correct names scheduled for correct dates
        print("RAs Scheduled Dates")
        for keys, RA in schedule_dict.items():
            print(keys, RA)
        print("-------------------------------------------")

        # confirm even distribution of worked day amounts/types
        print("RA Weekday/Weekend Counts")
        for keys, RA in RA_DETAILS.items():
            print(RA.name + " | Weekdays: " + str(RA.scheduled_weekdays) + " | Weekends: " + str(RA.scheduled_weekends))
        print("-------------------------------------------")

        # view partnerships for each RA for the given month
        print("RA Partnerships")
        for keys, RA in RA_DETAILS.items():
            print(RA.name + " | Partnerships: " + str(RA.partnerships) + " | " + str(len(RA.partnerships)) + "/" + str(len(RA_NAMES) - 1) + " RAs")
        print("-------------------------------------------")

        # view RA availability count for each RA for the given month
        print("RA Availability")
        for keys, RA in RA_DETAILS.items():
            print(RA.name + " | Availability: " + str(len(RA.availability_clean)) + "/" + str(NUM_DAYS_MONTH) + " days")
        print("-------------------------------------------")

        # create calendar with names of RAs on duty labeled on respective date
        calendar_create = MplCalendar(YEAR, MONTH_NUM)
        for DAY_NUM in range(SCHEDULE_START_DAY - 1, MONTH_END_DAY):
            if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
                for i in range(WEEKDAY_STAFF_NUM):
                    calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][i])
            elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
                for i in range(WEEKEND_STAFF_NUM):
                    calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][i])

        # duty schedule review instructions
        print("Once you are done reviewing the duty schedule, please exit out of the calendar pop-up window.")
        print("After closing the calendar pop-up window, you will be prompted to keep the current duty schedule or generate a new version.")
        input("Press ENTER to view the duty schedule.")
        calendar_create.show()

        # determine if scheduling for the current month or the next month
        user_satisfied = input("Would you like to KEEP (k) the current calendar or generate a NEW (n) version? [k/n]: ")
        if user_satisfied != 'k' and user_satisfied != 'n':
            print("ERROR: Please enter 'k' to keep the current duty schedule or 'n' to generate a new version.")
            sys.exit(1)

    # save the calendar image to the corrsponding directory
    calendar_save_path = MONTH_STRING + "_" + str(YEAR) + "_duty_schedule_" + BUILDING
    calendar_create.save("Schedule/" + calendar_save_path)

    # reset cumulative weekdays/weekends
    print("***Please enter 'n' if this is mid-academic year, you should only reset cumulative worked weekdays/weekends to 0 at the beginning or end of an academic year.***")
    reset = input("Would you like to reset cumulative worked weekdays/weekends for all RAs? [y/n]: ")

    # update History XLSX file
    for index, RA in enumerate(RA_DETAILS.values()):
        history_master.loc[index, "Weekdays Total"] = RA.scheduled_weekdays
        history_master.loc[index, "Weekends Total"] = RA.scheduled_weekends

        if reset == 'y':
            history_master.loc[index, "Weekdays Total"] = 0
            history_master.loc[index, "Weekends Total"] = 0

    # remove old History XLSX file and save new History XLSX file for future additions
    os.remove(HISTORY_FILE_PATH)
    history_master.to_excel(HISTORY_FILE_PATH, index=False)


def schedule_current_day(RA_DETAILS, DAY_NUM, weekday):
    count_threshold = NUM_DAYS_YEAR
    candidates = []
    candidate_guaranteed = None

    if weekday:
        CURRENT_DAY_STAFF_NUM = WEEKDAY_STAFF_NUM
    else:
        CURRENT_DAY_STAFF_NUM = WEEKEND_STAFF_NUM

    for keys, RA in RA_DETAILS.items():
        if weekday:
            CURRENT_DAY_TYPE_SCHEDULED_COUNT = RA.scheduled_weekdays
        else:
            CURRENT_DAY_TYPE_SCHEDULED_COUNT = RA.scheduled_weekends

        if CURRENT_DAY_TYPE_SCHEDULED_COUNT < count_threshold:
            count_threshold = CURRENT_DAY_TYPE_SCHEDULED_COUNT

    while len(candidates) < CURRENT_DAY_STAFF_NUM:
        for keys, RA in RA_DETAILS.items():
            if weekday:
                CURRENT_DAY_TYPE_SCHEDULED_COUNT = RA.scheduled_weekdays
            else:
                CURRENT_DAY_TYPE_SCHEDULED_COUNT = RA.scheduled_weekends

            if CURRENT_DAY_TYPE_SCHEDULED_COUNT <= count_threshold and DAY_NUM + 1 in RA.availability_clean and RA.name not in candidates:
                if DAY_NUM > 2:
                    if not (RA.name in schedule_dict[DAY_NUM] or RA.name in schedule_dict[DAY_NUM - 1] or RA.name in schedule_dict[DAY_NUM - 2]):
                        candidates.append(RA.name)
                else:
                    candidates.append(RA.name)
        if len(candidates) == 1 and not candidate_guaranteed:
            candidate_guaranteed = candidates[0]
        count_threshold += 1

        if count_threshold == NUM_DAYS_YEAR:
            print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " - Currently have " + str(len(candidates)) + " candidate(s) | Candidate(s): " + str(candidates))
            sys.exit(1)

    # update partnerships
    if len(candidates) == CURRENT_DAY_STAFF_NUM:
        if CURRENT_DAY_STAFF_NUM > 1:
            for i in range(len(candidates)):
                if not i and candidates[i] not in RA_DETAILS[candidates[0]].partnerships:
                    RA_DETAILS[candidates[0]].partnerships.append(candidates[i])
                    RA_DETAILS[candidates[i]].partnerships.append(candidates[0])
        else:
            pass  # no partnerships updated if alone

        # update day type counts
        for i in range(len(candidates)):
            if weekday:
                RA_DETAILS[candidates[i]].scheduled_weekdays += 1
            else:
                RA_DETAILS[candidates[i]].scheduled_weekends += 1

        # append RA names to the schedule management dictionary
        candidates_selected = []
        for i in range(len(candidates)):
            candidates_selected.append(candidates[i])

        schedule_dict[DAY_NUM + 1] = candidates_selected

    # scheduling process
    elif len(candidates) > CURRENT_DAY_STAFF_NUM:
        candidate_selection = random.sample(range(0, len(candidates)), len(candidates))
        if not candidate_guaranteed:
            candidates_selected = [candidates[candidate_selection[0]]]
            for index in range(1, len(candidate_selection)):
                if len(candidates_selected) != CURRENT_DAY_STAFF_NUM:
                    if candidates[candidate_selection[index]] not in RA_DETAILS[candidates[candidate_selection[0]]].partnerships:
                        RA_DETAILS[candidates[candidate_selection[0]]].partnerships.append(candidates[candidate_selection[index]])
                        RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidates[candidate_selection[0]])
                        candidates_selected.append(candidates[candidate_selection[index]])
                        break
            if len(candidates_selected) != CURRENT_DAY_STAFF_NUM:
                for index in range(1, len(candidate_selection)):
                    if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != WEEKEND_STAFF_NUM:
                        candidates_selected.append(candidates[candidate_selection[index]])
                        break

            # update weekend counts
            for i in range(len(candidates_selected)):
                if weekday:
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekdays += 1
                else:
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekends += 1

            # append RA names to the schedule management dictionary
            schedule_dict[DAY_NUM + 1] = candidates_selected
        else:
            candidates_selected = []
            for index in range(0, len(candidate_selection)):
                if len(candidates_selected) != CURRENT_DAY_STAFF_NUM - 1:
                    if candidates[candidate_selection[index]] not in RA_DETAILS[candidate_guaranteed].partnerships \
                            and not candidate_guaranteed == candidates[candidate_selection[index]]:
                        RA_DETAILS[candidate_guaranteed].partnerships.append(candidates[candidate_selection[index]])
                        RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidate_guaranteed)
                        candidates_selected.append(candidates[candidate_selection[index]])
                        break
            if len(candidates_selected) != CURRENT_DAY_STAFF_NUM - 1:
                for index in range(0, len(candidate_selection)):
                    if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != CURRENT_DAY_STAFF_NUM - 1 \
                            and not candidate_guaranteed == candidates[candidate_selection[index]]:
                        candidates_selected.append(candidates[candidate_selection[index]])
                        break

            # update day type counts
            for i in range(len(candidates_selected)):
                if weekday:
                    RA_DETAILS[candidate_guaranteed].scheduled_weekdays += 1
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekdays += 1
                else:
                    RA_DETAILS[candidate_guaranteed].scheduled_weekends += 1
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekends += 1

            # append RA names to the schedule management dictionary
            candidates_selected.append(candidate_guaranteed)
            schedule_dict[DAY_NUM + 1] = candidates_selected


if __name__ == '__main__':
    main()
