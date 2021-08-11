# RA Duty Scheduler
# Copyright (c) 2021, David Peterson
#
# All rights reserved.


class ResidentAdviser:
    """ Resident Advisor Management Class
    Class to track each Resident Adviser's (RA's) availability, type of scheduled days, and more.
    """

    def __init__(self, name, availability):
        self.name = name                        # name of the RA
        self.availability_clean = availability  # list to hold dates for availability for duty for the given month
        # self.cleanAvailability()                # method call to remove dates the RA is not available

        self.scheduled_weekdays = 0             # count for number of weekdays an RA is scheduled in a month
        self.scheduled_weekends = 0             # count for number of weekends an RA is scheduled in a month
        self.scheduled_total = 0                # count for number of total days scheduled

        self.partnerships = []                  # list to hold names of RAs an RA has had duty with for the given month

    # method to create a list of dates the RA is available for the given month
    def cleanAvailability(self):
        for index, value in enumerate(self.availability_raw):
            if value != 'N' and value != 'n':
                self.availability_clean.append(index+1)
