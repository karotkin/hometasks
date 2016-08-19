#Case1_Dictionary
listkeys = [0, 1, 2, 3, 4, 5, 6]
listvalues = ['Name','Secondname','Surname','Height', 'Weight']
mydict = dict(zip(listkeys, listvalues + [None]*(len(listkeys)-len(listvalues))))
print (mydict)

#Case2_Polyndrome
str1 = input("Hello, enter your word here: ")
str2 = str1[::-1]
if str1 == str2:
    print("yes, this is polyndrome")
else:
    print("no, this is not polyndrome")

#Case3_Compare
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
result = list(set(a) & set(b))
print("There are simmilar elements in both:",result)

#Case4_Ipaddresses from access.log
file = open('access.log', 'r')
d = dict()
for line in file:
    ip = line.split()[0]
    if ip not in d:
        d[ip]=1
    else:
        d[ip]+=1
print(sorted(d,key=d.get, reverse=True)[:11])
