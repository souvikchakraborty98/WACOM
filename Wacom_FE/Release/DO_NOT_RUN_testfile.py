import matplotlib.pyplot as plt
import csv
import os
import mplcursors
from celluloid import Camera
import turtle
import math

# x = []
# y = []

# data=""
# f = open("filename.log", "r")

# for z in f:
#     data=data+z

# filenamelist=data.split("+")
# filenamecoord=filenamelist[0]
# filenamepress=filenamelist[1]

# with open(filenamecoord,'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(int(row[0]))
#         y.append(int(row[1]))

# plt.subplot(1,2,1)
# plt.scatter(x,y,label='xy plot')
# ax = plt.gca()
# ax.set_ylim(ax.get_ylim()[::-1])
# plt.xlabel('x pixels')
# plt.ylabel('y pixels')
# plt.title('Coordinate data Scatter plot')
# plt.legend()

# x = []

# with open(filenamepress,'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(int(row[0]))

# plt.subplot(1,2,2)
# plt.plot(x, label='xy plot')
# plt.xlabel('x pixels')
# plt.ylabel('y pixels')
# plt.title('Presssure data 2D plot')
# plt.legend()


# mng=plt.get_current_fig_manager()
# mng.window.state("zoomed")
# mplcursors.cursor(hover=True)
# plt.show()

# #os.startfile("Wacom Feature Extractor.exe")
# x=["Wacom Feature Extractor.exe","sadva","vaef"]

# if "Wacom Feature Extractor.exe" in x:
#      print("dawd")
spiral=turtle.Turtle()

wn=turtle.Screen()
spiral.color("blue")
wn.setup(1366,768)
spiral.ht()
spiral.penup()
for i in range(121):
    t = i / 20 * math.pi
    x = (1 + 18 * t) * math.cos(t)
    y = (1 + 18 * t) * math.sin(t)
    spiral.goto(x, y)
    spiral.dot(5)
spiral.up()
turtle.Screen().exitonclick()

