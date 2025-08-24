file= open("codingal.txt", "r")
print(file.read())
file.close()

file= open("codingal.txt", "r")
print("\n Read in parts \n")
print(file.read(8))
file.close()

file= open("codingal.txt", "a")
file.write("Hi! I am Penguin and i am 1 year old.")
file.close()