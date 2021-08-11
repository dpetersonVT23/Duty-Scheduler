# RA Duty Scheduler
# Copyright (c) 2021, David Peterson
#
# All rights reserved.


class ResidentAdviser:
    """ Resident Advisor Management Class
    Class to track each Resident Adviser's (RA's) availability, type of scheduled days, and more.
    """

    def __init__(self, name, availability, cum_wdays, cum_wends):
        self.name = name                        # name of the RA
        self.availability_raw = availability    # list to hold availabilities for each day of the month
        self.availability_clean = []            # list to hold dates for availability for duty for the given month
        self.cleanAvailability()                # method call to remove dates the RA is not available

        self.scheduled_weekdays = cum_wdays     # count for number of weekdays an RA is scheduled in a month
        self.scheduled_weekends = cum_wends     # count for number of weekends an RA is scheduled in a month

        self.partnerships = []                  # list to hold names of RAs an RA has had duty with for the given month

    # method to create a list of dates the RA is available for the given month
    def cleanAvailability(self):
        for index, value in enumerate(self.availability_raw):
            if value != 'N' and value != 'n':
                self.availability_clean.append(index+1)
