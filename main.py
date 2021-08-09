# RA Duty Scheduler
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
YEAR = datetime.today().year
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
WEEKENDS = ['Friday', 'Saturday']
NUM_DAYS_YEAR = 365

# setting number of RAs on duty weekday/weekend
WEEKDAY_STAFF_NUM = 2
WEEKEND_STAFF_NUM = 2

# month number and string
MONTH_NUM = datetime.today().month + 1 % 12
MONTH_STRING = calendar.month_name[MONTH_NUM]

# number of days in current month
NUM_DAYS_MONTH = calendar.monthrange(datetime.today().year, datetime.today().month + 1 % 12)[1]

# schedule bounds - useful for partial months of duty scheduling
SCHEDULE_START_DAY = 1
MONTH_END_DAY = NUM_DAYS_MONTH

# dictionary to hold names of RA scheduled for each date
schedule_dict = {}

for i in range(NUM_DAYS_MONTH):
    schedule_dict[i + 1] = ['RA']

# read and create Pandas data frame from Availability XLSX file
# CHANGE THE NAME OF YOUR AVAILABILITY XLSX FILE HERE
AVAILABILITY_FILE_PATH = "Availability/myAvailabilityExcelFile.xlsx"
availability_master = pd.DataFrame(pd.read_excel(AVAILABILITY_FILE_PATH))

#################
import pandas as pd
import calendar
from datetime import datetime

AVAILABILITY_FILE_PATH_OLD = "Availability/test1.xlsx"
availability_master = pd.DataFrame(pd.read_excel(AVAILABILITY_FILE_PATH_OLD))

# list of RA names from Availability XLSX file
RA_NAMES = availability_master["First Name"].tolist()

# list of days the RA's are busy
RA_BUSY_DAYS = availability_master["Days"].tolist()

# number of days in current month
NUM_DAYS_MONTH = calendar.monthrange(datetime.today().year, datetime.today().month + 1 % 12)[1]

columns = ["RA Name"]
for m in range(1, NUM_DAYS_MONTH+1):
    columns.append(str(m))

busy_dict = {}
availability_dict = {}

for i in range(len(RA_NAMES)):
    days_ints = []
    days_ints_strings = []
    default = []
    days_strings = RA_BUSY_DAYS[i]
    days_strings_split = days_strings.split("/")

    for j in range(len(days_strings_split)):
        if j % 2:
            days_ints_strings.append(days_strings_split[j])
    busy_dict[RA_NAMES[i]] = days_ints_strings

    for k in range(len(days_ints_strings)):
        days_ints.append(int(days_ints_strings[k]))

    for l in range(1, NUM_DAYS_MONTH+1):
        if l not in days_ints:
            default.append(l)

############



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
    candidate_selected = None
    candidate_guaranteed = None
    weekday_boolean = True

    # candidate selection
    if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
        weekday_boolean = True
        for keys, RA in RA_DETAILS.items():
            if RA.scheduled_weekdays < count_threshold:
                count_threshold = RA.scheduled_weekdays
        while len(candidates) < WEEKDAY_STAFF_NUM:
            for keys, RA in RA_DETAILS.items():
                if RA.scheduled_weekdays <= count_threshold and DAY_NUM + 1 in RA.availability_clean and RA.name not in candidates:
                    if DAY_NUM:
                        if RA.name not in schedule_dict[DAY_NUM]:
                            candidates.append(RA.name)
                    else:
                        candidates.append(RA.name)
            if len(candidates) == 1 and not candidate_guaranteed:
                candidate_guaranteed = candidates[0]
            count_threshold += 1

            if count_threshold == NUM_DAYS_YEAR:
                print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " (WEEKDAY) - Currently have " + str(len(candidates)) + " candidate(s) | Candidate(s): " + str(candidates))
                sys.exit(1)

        # update partnerships
        if len(candidates) == WEEKDAY_STAFF_NUM:
            if WEEKEND_STAFF_NUM > 1:
                for i in range(len(candidates)):
                    if not i and candidates[i] not in RA_DETAILS[candidates[0]].partnerships:
                        RA_DETAILS[candidates[0]].partnerships.append(candidates[i])
                        RA_DETAILS[candidates[i]].partnerships.append(candidates[0])
            else:
                pass  # no partnerships updated if alone

            # update weekday counts
            for i in range(len(candidates)):
                RA_DETAILS[candidates[i]].scheduled_weekdays += 1

            # append RA names to the schedule management dictionary
            candidates_selected = []
            for i in range(len(candidates)):
                candidates_selected.append(candidates[i])

            schedule_dict[DAY_NUM + 1] = candidates_selected

        # scheduling process
        elif len(candidates) > WEEKDAY_STAFF_NUM:
            candidate_selection = random.sample(range(0, len(candidates)), len(candidates))
            if not candidate_guaranteed:
                candidates_selected = [candidates[candidate_selection[0]]]
                for index in range(1, len(candidate_selection)):
                    if len(candidates_selected) != WEEKDAY_STAFF_NUM:
                        if candidates[candidate_selection[index]] not in RA_DETAILS[candidates[candidate_selection[0]]].partnerships:
                            RA_DETAILS[candidates[candidate_selection[0]]].partnerships.append(candidates[candidate_selection[index]])
                            RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidates[candidate_selection[0]])
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break
                if len(candidates_selected) != WEEKDAY_STAFF_NUM:
                    for index in range(1, len(candidate_selection)):
                        if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != WEEKDAY_STAFF_NUM:
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break

                # update weekday counts
                for i in range(len(candidates_selected)):
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekdays += 1

                # append RA names to the schedule management dictionary
                schedule_dict[DAY_NUM + 1] = candidates_selected
            else:
                candidates_selected = []
                for index in range(0, len(candidate_selection)):
                    if len(candidates_selected) != WEEKDAY_STAFF_NUM-1:
                        if candidates[candidate_selection[index]] not in RA_DETAILS[candidate_guaranteed].partnerships \
                                and not candidate_guaranteed == candidates[candidate_selection[index]]:
                            RA_DETAILS[candidate_guaranteed].partnerships.append(candidates[candidate_selection[index]])
                            RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidate_guaranteed)
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break
                if len(candidates_selected) != WEEKDAY_STAFF_NUM-1:
                    for index in range(0, len(candidate_selection)):
                        if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != WEEKDAY_STAFF_NUM-1 \
                                and not candidate_guaranteed == candidates[candidate_selection[index]]:
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break

                # update weekday counts
                for i in range(len(candidates_selected)):
                    RA_DETAILS[candidate_guaranteed].scheduled_weekdays += 1
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekdays += 1

                # append RA names to the schedule management dictionary
                candidates_selected.append(candidate_guaranteed)
                schedule_dict[DAY_NUM + 1] = candidates_selected
    elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
        weekday_boolean = False
        for keys, RA in RA_DETAILS.items():
            if RA.scheduled_weekends < count_threshold:
                count_threshold = RA.scheduled_weekends
        while len(candidates) < WEEKEND_STAFF_NUM:
            for keys, RA in RA_DETAILS.items():
                if RA.scheduled_weekends <= count_threshold and DAY_NUM + 1 in RA.availability_clean and RA.name not in candidates:
                    if DAY_NUM:
                        if RA.name not in schedule_dict[DAY_NUM]:
                            candidates.append(RA.name)
                    else:
                        candidates.append(RA.name)
            if len(candidates) == 1 and not candidate_guaranteed:
                candidate_guaranteed = candidates[0]
            count_threshold += 1

            if count_threshold == NUM_DAYS_YEAR:
                print("NOT ENOUGH CANDIDATES FOR " + MONTH_STRING + " " + str(DAY_NUM + 1) + " (WEEKEND) - Currently have " + str(len(candidates)) + " candidate(s) | Candidate(s): " + str(candidates))
                sys.exit(1)

        # update partnerships
        if len(candidates) == WEEKEND_STAFF_NUM:
            if WEEKEND_STAFF_NUM > 1:
                for i in range(len(candidates)):
                    if not i and candidates[i] not in RA_DETAILS[candidates[0]].partnerships:
                        RA_DETAILS[candidates[0]].partnerships.append(candidates[i])
                        RA_DETAILS[candidates[i]].partnerships.append(candidates[0])
            else:
                pass  # no partnerships updated if alone

            # update weekend counts
            for i in range(len(candidates)):
                RA_DETAILS[candidates[i]].scheduled_weekends += 1

            # append RA names to the schedule management dictionary
            candidates_selected = []
            for i in range(len(candidates)):
                candidates_selected.append(candidates[i])

            schedule_dict[DAY_NUM + 1] = candidates_selected

        # scheduling process
        elif len(candidates) > WEEKEND_STAFF_NUM:
            candidate_selection = random.sample(range(0, len(candidates)), len(candidates))
            if not candidate_guaranteed:
                candidates_selected = [candidates[candidate_selection[0]]]
                for index in range(1, len(candidate_selection)):
                    if len(candidates_selected) != WEEKEND_STAFF_NUM:
                        if candidates[candidate_selection[index]] not in RA_DETAILS[candidates[candidate_selection[0]]].partnerships:
                            RA_DETAILS[candidates[candidate_selection[0]]].partnerships.append(candidates[candidate_selection[index]])
                            RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidates[candidate_selection[0]])
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break
                if len(candidates_selected) != WEEKEND_STAFF_NUM:
                    for index in range(1, len(candidate_selection)):
                        if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != WEEKEND_STAFF_NUM:
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break

                # update weekend counts
                for i in range(len(candidates_selected)):
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekends += 1

                # append RA names to the schedule management dictionary
                schedule_dict[DAY_NUM + 1] = candidates_selected
            else:
                candidates_selected = []
                for index in range(0, len(candidate_selection)):
                    if len(candidates_selected) != WEEKEND_STAFF_NUM - 1:
                        if candidates[candidate_selection[index]] not in RA_DETAILS[candidate_guaranteed].partnerships \
                                and not candidate_guaranteed == candidates[candidate_selection[index]]:
                            RA_DETAILS[candidate_guaranteed].partnerships.append(candidates[candidate_selection[index]])
                            RA_DETAILS[candidates[candidate_selection[index]]].partnerships.append(candidate_guaranteed)
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break
                if len(candidates_selected) != WEEKEND_STAFF_NUM - 1:
                    for index in range(0, len(candidate_selection)):
                        if candidates[candidate_selection[index]] not in candidates_selected and len(candidates_selected) != WEEKEND_STAFF_NUM - 1 \
                                and not candidate_guaranteed == candidates[candidate_selection[index]]:
                            candidates_selected.append(candidates[candidate_selection[index]])
                            break

                # update weekend counts
                for i in range(len(candidates_selected)):
                    RA_DETAILS[candidate_guaranteed].scheduled_weekends += 1
                    RA_DETAILS[candidates[candidate_selection[i]]].scheduled_weekends += 1

                # append RA names to the schedule management dictionary
                candidates_selected.append(candidate_guaranteed)
                schedule_dict[DAY_NUM + 1] = candidates_selected

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
for DAY_NUM in range(NUM_DAYS_MONTH):
    if calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKDAYS:
        for i in range(WEEKDAY_STAFF_NUM):
            calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][i])
    elif calendar.day_name[datetime(YEAR, MONTH_NUM, DAY_NUM + 1).weekday()] in WEEKENDS:
        for i in range(WEEKEND_STAFF_NUM):
            calendar_create.add_event(DAY_NUM + 1, schedule_dict[DAY_NUM + 1][i])
calendar_create.show()

calendar_save_path = MONTH_STRING + "_" + str(YEAR) + "_duty_schedule"
calendar_create.save("Schedule/" + calendar_save_path)
