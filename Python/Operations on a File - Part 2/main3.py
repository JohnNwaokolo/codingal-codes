with open("file1.txt", "w") as f1:
    f1.write("Hello, this is f1 content.")
f1.close()

with open("file2.txt", "w") as f2:
    f2.write("Hello, this is f2 content.")
f2.close()

f3= open("file3.txt", "w")
f3.close()

f1= open("file1.txt", "r")
f2= open("file2.txt", "r")
f3= open("file3.txt", "w")

f3.write(f1.read())
f3.write(f2.read())

f1.close()
f2.close()
f3.close()
