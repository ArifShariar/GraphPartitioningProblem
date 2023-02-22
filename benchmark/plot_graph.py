import pandas
import matplotlib.pyplot as plt
# read csv file
df = pandas.read_csv('../data/FM_Benchmark_2.csv')
print(df.head())

# plot graph of number of vertices vs Time
x = df['Number Of Vertices']
y = df['Time (micro seconds)']
plt.plot(x, y)
plt.xlabel('Number Of Vertices')
plt.ylabel('Time (micro seconds)')
plt.title('Number Of Vertices vs Time')
plt.savefig('../benchmark/Number Of Vertices vs Time FM Algo.png')
plt.show()


x1 = df['Number of Edges']
y1 = df['Time (micro seconds)']
plt.plot(x1, y1)
plt.xlabel('Number of Edges')
plt.ylabel('Time (micro seconds)')
plt.title('Number of Edges vs Time')
plt.savefig('../benchmark/Number of Edges vs Time FM Algo.png')
plt.show()