#this file will hold the object query tracker which
#will be ascociated with an api key to make sure that
#no more than 1500 calls are made within a rolling 30
#second window

#IMPORTS
import time

class QuereyManager:
    def __init__(self):
        self.last30Seconds = []
    
    def waitUntilGoodToCommit(self):
        """
        Holds program until the number of times this function has been called
        in the last rolling 30 seconds is under 500.
        """
        while(True):
            if len(self.last30Seconds) < 500:
                self.last30Seconds.append(time.perf_counter())
                print(len(self.last30Seconds))
                return
            else:
                if (time.perf_counter() - self.last30Seconds[0]) > 30.0:
                    self.last30Seconds.pop(0)
                    print("pop!")
                else:
                    print("Too many calls! Calls made in last 30 seconds:", len(self.last30Seconds), "Sleeping for", int((self.last30Seconds[0] - time.perf_counter() )+30),"seconds.")
                    print(int(time.perf_counter()-self.last30Seconds[0]), int(time.perf_counter()-self.last30Seconds[-1]), int(time.perf_counter()-self.last30Seconds[-2]), int(time.perf_counter()-self.last30Seconds[-3]))
                    time.sleep((self.last30Seconds[0] - time.perf_counter() )+30)




"""#testing code:
testTime = QuereyManager()
for i in range(1001) :
    testTime.waitUntilGoodToCommit()"""