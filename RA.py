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
        self.availability_clean = availability  # list to hold dates for availability for duty for the given month

        self.scheduled_weekdays = cum_wdays     # count for number of weekdays an RA is scheduled in a month
        self.scheduled_weekends = cum_wends     # count for number of weekends an RA is scheduled in a month

        self.partnerships = []                  # list to hold names of RAs an RA has had duty with for the given month
