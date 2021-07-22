# David Peterson
# file to manage ResidentAdvisor class

# import statements


class ResidentAdvisor:
    """ Resident Advisor Management Class
    Class to track each Resident Advisor's (RA's) availability, type of scheduled days, and more.
    """

    def __init__(self, name, availability):
        self.name = name
        self.availability_raw = availability
        self.availability_clean = []
        self.cleanAvailability()

        self.scheduled_weekdays = 0
        self.scheduled_weekends = 0

    def cleanAvailability(self):
        for index, value in enumerate(self.availability_raw):
            if value != 'N' and value != 'n':
                self.availability_clean.append(index+1)
