#read data from a text file and output into a csv file
#first line of the text file is column names of the csv file


import csv
import sys

def read_data(filename):
    file = open(filename, 'r')
    data = []
    for line in list(file):
        v_list = line.split()
        data.append(v_list)
    return data

def write_data(filename, data):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
        

if __name__ == "__main__": 
    data = read_data("outputrecord.txt")
    write_data("KL_benchmark.csv", data)

