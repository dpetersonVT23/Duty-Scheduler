# Duty Scheduler
# Copyright (c) 2021, David Peterson
#
# All rights reserved.


class StaffMember:
    """ Staff Member Management Class
    Class to track each staff member's availability, type of scheduled days, and more.
    """

    def __init__(self, name, availability, cum_wdays, cum_wends):
        self.name = name                        # name of the staff member
        self.availability_clean = availability  # list to hold dates for availability for duty for the given month

        self.scheduled_weekdays = cum_wdays     # count for number of weekdays a staff member is scheduled in a month
        self.scheduled_weekends = cum_wends     # count for number of weekends a staff member is scheduled in a month

        self.partnerships = []                  # list to hold names of other staff members a staff member has had duty with for the given month
