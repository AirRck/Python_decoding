#Jakub Kaminski
import re

class  EventsAnalyzer:
    hourRegex = re.compile('\\d\\d:\\d\\d')
    dateRegex = re.compile('(\\d{2}/\\d{2}/\\d{4})|(\\d{4}/\\d{2}/\\d{2})')

    def __init__(self, input):
        """
        :type input: str
        """
        self.events = {}
        for line in input.splitlines():
            self.__decodeLine(line)

    def __decodeLine(self, line):
        """
        :type line: str
        """
        hourMatch = EventsAnalyzer.hourRegex.search(line)
        hour = hourMatch.group(0)

        dateMatch = EventsAnalyzer.dateRegex.search(line)
        date = dateMatch.group(0)

        line = line[:hourMatch.start(0)] + (" " * len(hour)) + line[hourMatch.end(0):]
        line = line[:dateMatch.start(0)] + (" " * len(date)) + line[dateMatch.end(0):]


        eventName = " ".join(line.split())
        # "asdas" -> [(12312), (12312, 123), ]
        #

        self.events.setdefault(eventName, [])
        self.events[eventName].append((date, hour))

    def show_events(self):
        for key in sorted(self.events.keys()):
            print(key + ":")
            for timeDate in self.events[key]:
                print(timeDate)

    def __getitem__(self, eventName):
        """
        :type eventName: str
        """
        return self.events[eventName]
