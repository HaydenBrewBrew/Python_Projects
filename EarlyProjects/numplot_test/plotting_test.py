#%%
#basic testing code for understanding how to plot using matplotlib and numpy
import numpy as np 
import matplotlib.pyplot as plt
import random

# initial plotting test using
fig, ax = plt.subplots() #create a figure
p = [1,2,3,4]
ax.plot(p,[1,4,3,2])


# %%
# Test using Bar Graphs
n = 5 
menMeans = (20,35,30,35,27)
womenMeans = (25,32,34,20,25)
menStd = (2,3,4,1,2)
womenStd = (3,5,2,3,3)
ind = np.arange(n)#sets x location numbers
width = 0.35 #bar width
#Set up the plots one for men and then overlay the women on top
p1 = plt.bar(ind, menMeans, width, yerr=menStd)
p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

#labeling of the graph
plt.ylabel('Scores')
plt.title('Scores by Group and Gender')
plt.xticks(ind, ('G1','G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 80,8))
plt.legend((p1[0], p2[0]), ('Men', 'Women'))


# %%
