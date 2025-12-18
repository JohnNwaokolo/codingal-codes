with open("codingal.txt", "w") as file:
    file.write("Heyy, I am John.")
file.close()    

with open("codingal.txt", "r") as file:
    data = file.readlines()
    print("The file divided into words: ")
    for line in data:
        word = line.split()
        print(word)
file.close()        