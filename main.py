# RA Duty Scheduler 2021
# Copyright (c) 2021, David Peterson
#
# All rights reserved.

# import statements
import calendar
import pandas as pd
import sys
import random

from datetime import datetime
from RA import ResidentAdviser
from mplcal import MplCalendar

# constants
YEAR = 2021
MIN_SCHEDULED_RAS = 2
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
WEEKENDS = ['Friday', 'Saturday']
NUM_DAYS_YEAR = 365

# month number and string
MONTH_NUM = datetime.today().month
MONTH_STRING = calendar.month_name[MONTH_NUM]

# number of days in current month
NUM_DAYS_MONTH = calendar.monthrange(datetime.today().year, datetime.today().month)[1]

# schedule bounds - useful for partial months of duty scheduling
SCHEDULE_START_DAY = 1
MONTH_END_DAY = NUM_DAYS_MONTH

# dictionary to hold names of RA scheduled for each date
schedule_dict = {}

for i in range(NUM_DAYS_MONTH):
    schedule_dict[i + 1] = ['RA1', 'RA2']

# read and create Pandas data frame from Availability XLSX file
# CHANGE THE NAME OF YOUR AVAILABILITY XLSX FILE HERE
AVAILABILITY_FILE_PATH = "Availability/test1.xlsx"
availability_master = pd.DataFrame(pd.read_excel(AVAILABILITY_FILE_PATH))

# list of RA names from Availability XLSX file
RA_NAMES = availability_master["RA Name"].tolist()

# create RA object from ResidentAdviser class for each RA in Availability XLSX file
RA_DETAILS = {}
for i in range(len(RA_NAMES)):
    RA_DETAILS[RA_NAMES[i]] = ResidentAdviser(RA_NAMES[i], availability_master.iloc[i, SCHEDULE_START_DAY:MONTH_END_DAY + 1].tolist())

# determine candidates for scheduling on each day of the current month + schedule accordingly based on availability
for DAY_NUM in range(NUM_DAYS_MONTH):
    count_threshold = NUM_DAYS_YEAR
    candidates = []
    weekday_boolean = True

    # candidate selection
    if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
        weekday_boolean = True
        for keys, RA in RA_DETAILS.items():
            if RA.scheduled_weekdays < count_threshold:
                count_threshold = RA.scheduled_weekdays
        while len(candidates) < MIN_SCHEDULED_RAS:
            for keys, RA in RA_DETAILS.items():
                if RA.scheduled_weekdays <= count_threshold and DAY_NUM + 1 in RA.availability_clean and RA.name not in candidates:
                    candidates.append(RA.name)
            count_threshold += 1

            if count_threshold == NUM_DAYS_YEAR:
                print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " (WEEKDAY)")
                sys.exit(1)
    elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
        weekday_boolean = False
        for keys, RA in RA_DETAILS.items():
            if RA.scheduled_weekends < count_threshold:
                count_threshold = RA.scheduled_weekends
        while len(candidates) < MIN_SCHEDULED_RAS:
            for keys, RA in RA_DETAILS.items():
                if RA.scheduled_weekends <= count_threshold and DAY_NUM + 1 in RA.availability_clean and RA.name not in candidates:
                    candidates.append(RA.name)
            count_threshold += 1

            if count_threshold == NUM_DAYS_YEAR:
                print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " (WEEKEND) - Currently have " + str(len(candidates)) + " candidate(s)")
                sys.exit(1)

    # scheduling process
    candidate_selection = random.sample(range(0, len(candidates)), 2)

    if weekday_boolean:
        RA_DETAILS[candidates[candidate_selection[0]]].scheduled_weekdays += 1
        RA_DETAILS[candidates[candidate_selection[1]]].scheduled_weekdays += 1
    else:
        RA_DETAILS[candidates[candidate_selection[0]]].scheduled_weekends += 1
        RA_DETAILS[candidates[candidate_selection[1]]].scheduled_weekends += 1

    # append RA names to the schedule management dictionary
    schedule_dict[DAY_NUM + 1] = candidates[candidate_selection[0]], candidates[candidate_selection[1]]

# confirm correct names scheduled for correct dates
# for keys, RA in schedule_dict.items():
#     print(keys, RA)

# confirm even distribution of worked day amounts/types
for keys, RA in RA_DETAILS.items():
    print(RA.name + " | Weekdays: " + str(RA.scheduled_weekdays) + " | Weekends: " + str(RA.scheduled_weekends))

# create calendar with names of RAs on duty labeled on respective date
calendar_create = MplCalendar(YEAR, MONTH_NUM)
for DAY_NUM in range(NUM_DAYS_MONTH):
    calendar_create.add_event(DAY_NUM+1, schedule_dict[DAY_NUM + 1][0])
    calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][1])
calendar_create.show()

calendar_save_path = MONTH_STRING + "_" + str(YEAR) + "_duty_schedule"
calendar_create.save("Schedule/" + calendar_save_path)
