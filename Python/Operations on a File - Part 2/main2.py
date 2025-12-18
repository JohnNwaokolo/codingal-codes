# new_file = open("New-file.txt", "x")
# new_file.close()

import os
print("Checking if a file exists. ")
if os.path.exists("my_file.txt"):
    os.remove("my_file.txt")
    print("Removed file")
else:
    print("File doesn't exist")

os.rmdir("experiment")