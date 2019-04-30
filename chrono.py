from math import floor


class Chrono:  # Time, in seconds since midnight
    def __init__(self, start, step=60):
        self.time = start
        self.step = step

    def tick(self, time=0):
        if time:
            self.time += time
        else:
            self.time += self.step

    def convertToSeconds(self, time, format):
        if format == "second":
            return time
        elif format == "minute":
            return time * 60
        elif format == "hour":
            return time * 3600

    def getTime(self, format):
        if format == "second":
            return self.time
        elif format == "minute":
            return self.time / 60
        elif format == "hour":
            return self.time / 3600
        elif format == "clock":
            hours = floor(self.time / 3600)
            minutes = floor((self.time - (3600 * hours)) / 60)
            seconds = self.time - (3600 * hours) - (60 * minutes)
            return [hours, minutes, seconds]


TIME = Chrono(33600, step=60)  # Start time at 5AM, 5 minutes at a time)
