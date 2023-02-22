import pandas
import matplotlib.pyplot as plt
# read csv file
df = pandas.read_csv('KL_benchmark.csv')
print(df.head())

# plot graph of number of vertices vs Time
#sort by number of vertices
df = df.sort_values(by=['No. of Vertices'])

x = df['No. of Vertices']
y = df['time(seconds)']
plt.plot(x, y)
plt.xlabel('Number Of Vertices')
plt.ylabel('Time (seconds)')
plt.title('Number Of Vertices vs Time')
plt.savefig('../benchmark/Number Of Vertices vs Time KL Algo.png')
plt.show()


#sort by number of edges
df = df.sort_values(by=['No. of Edges'])

x1 = df['No. of Edges']
y1 = df['time(seconds)']
plt.plot(x1, y1)
plt.xlabel('Number of Edges')
plt.ylabel('Time (seconds)')
plt.title('Number of Edges vs Time')
plt.savefig('../benchmark/Number of Edges vs Time KL Algo.png')
plt.show()