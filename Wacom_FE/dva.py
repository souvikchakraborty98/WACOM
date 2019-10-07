import matplotlib.pyplot as plt
import csv
import subprocess
import mplcursors

x = []
y = []

with open('fbs.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

# fig_size = plt.rcParams["figure.figsize"]
# fig_size[0] = 14
# fig_size[1] = 5
# plt.rcParams["figure.figsize"] = fig_size

plt.subplot(1,2,1)
plt.scatter(x,y,label='xy plot')
plt.xlabel('x pixels')
plt.ylabel('y pixels')
plt.title('Coordinate data Scatter plot')
plt.legend()

x = []

with open('pbs.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))

plt.subplot(1,2,2)
plt.plot(x, label='xy plot')
plt.xlabel('x pixels')
plt.ylabel('y pixels')
plt.title('Presssure data 2D plot')
plt.legend()
mng=plt.get_current_fig_manager()
mng.window.state("zoomed")
mplcursors.cursor(hover=True)
plt.show()

#subprocess.call(["Wacom Feature Extractor.exe"])
