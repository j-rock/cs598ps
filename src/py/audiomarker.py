

class AudioMarker():
    """
    AudioMarker - used to contain the minute and second of an event
    """

    def __init__(self,min,sec):
        self.min = min
        self.sec = sec

    def getMin(self):
        return self.min

    def getSec(self):
        return self.sec

    def __str__(self):
        return "{0:02d}:{1:02d}".format(self.min,self.sec)
