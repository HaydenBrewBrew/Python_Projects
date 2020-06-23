msg = "sup cuck"
msg2 = msg.upper()
msg_bool= msg2.isupper()
print(msg_bool)
#some basic string control sequences for Testing
print("_______String Length________")
msg_length1  =  len(msg)
msg_length2 = len(msg2)
print(msg_length1)
print(msg_length2)
# Divided up the string and mess with it 
msg_split = msg.split(" ")
#shallow copy
msg_split2 =  msg_split[:]
m1 = msg_split.pop(0)
m3 = msg_split2.pop(0)
if id(m1) == id(m3):
    print("Locations Copied")
print("_____Split Up String___")
print(m1)
print(msg_split)
m2 = msg_split.pop(0)
print(m2)
print("___Shallow Copy_____")
## This should be empty but its because i am popping references 
print(msg_split2)

## Test Abhi's idea

List = [1 , 2, 3, 4, 5]
print("___List___")
print(List)
listval = List.pop(1)
print("__Popped Value___")
print(listval)
print("____New List___")
print(List)
listval = List.pop(0)
print(List)