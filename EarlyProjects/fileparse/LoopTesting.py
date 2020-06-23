#This is a basic script for practicing the syntax for different loops in python 
import sys

class TestClass:
    i = 1
    def __init__(self):
        self.i = 10000

    def set_i(self, j):
        print(j)
        temp = self.i
        self.i = j
        print(temp)
        return(temp)

if (len(sys.argv) < 2):
    argv = 1
else:
    argv = sys.argv[1]
print(argv)

#for loop using a restricted range
for x in range(0,int(argv)):
    print("X Value: %d" % (x))

#For each loop throgh an array

for y in [ 5, 10, 15]:
    print("Y value: %d" % (y))

#for loop with strings
for f in ["TEST1", "TEST2", "TEST3", "TEST4", "TEST5"]:
    print(f.capitalize())
t = 0
while (t < 100):
    t += 1
    if (t % 10 == 0):
        print(t)

clsc = TestClass()
clsc.set_i(100)


        