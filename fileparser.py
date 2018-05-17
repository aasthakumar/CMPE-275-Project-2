import csv
import time
import multiprocessing
import sys

def seq():
    print("runing seq")
    start_time = time.time()
    f = open('GrammarandProductReviews.csv',"r")
    csv_f = csv.reader(f)
    for row in csv_f:
        results = process_line(row)
        print(results)
    print("seq --- time:{0:.4f}".format(time.time() - start_time))
    #print "seq --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)

def par():
    print("runing par")
    start_time = time.time()
    with open("GrammarandProductReviews.csv", "r") as source_file:
        results =  multiprocessing.Pool(processes=16).map(process_line, source_file, 4)
    print(results) 
    print("par --- time:{0:.4f}".format(time.time() - start_time))

def process_line(line):
    time.sleep(.01)
    return "FOO: %s" % line


if __name__ == "__main__":    
    #seq()
    par()