#read all the text file from a f line by line, split each line into a list of words, and then write them to another file
#

f2 = open('data16.txt', 'w')

with open('graph_500_5000_4.txt', 'r') as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        if(count < 2):
            count += 1
            continue
        words = line.split()  
        f2.write(words[1] +" "+ words[2]+'\n')
