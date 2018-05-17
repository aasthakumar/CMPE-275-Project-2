import threading
import queue
import time
#Number of threads
n_thread = 5
#Create queue
queue = queue.Queue()

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
    #Assign thread working with queue
        self.queue = queue

    def run(self):
        while True:
        #Get from queue job
            host = self.queue.get()
            print(self.getName() + ":" + host)
        #signals to queue job is done
            self.queue.task_done()

#Create number process
for i in range(n_thread):
    t = ThreadClass(queue)
    t.setDaemon(True)
    #Start thread
    t.start()

#Read file line by line
print("runing threaded")
start_time = time.time()
hostfile = open("GrammarandProductReviews.csv","r")
for line in hostfile:
    #Put line to queue
    time.sleep(.01)
    queue.put(line)
#wait on the queue until everything has been processed 
queue.join()
print("threaded --- time:{0:.4f}".format(time.time() - start_time))
