file= open("codingal.txt", "r")
print("Reading first line...")
print(file.readline())
file.close()

file= open("codingal.txt", "r")
print("Reading multiple lines....")
print(file.readline())
print(file.readline())
print(file.readline())
file.close()

file =open("codingal.txt", "r")
for line in file: 
    print(line)
file.close()