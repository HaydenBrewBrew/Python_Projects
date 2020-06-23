file = open("./TestFiles/Test.txt", 'r')
##print all way 1
for each in file:
    print(each)

file.seek(0) # return file pointer to the top of the file
## print all way 2 
print (file.read())
file.close()
## Edit the file
file = open("./TestFiles/Test.txt", 'w')
file.seek(0)
file.write("This has been added")
file.flush()
file.close()

