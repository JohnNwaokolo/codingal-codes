first_name = input("Input your first name: ")
last_name = input("Input your last name: ")

gender = ["Male", "Female", "Other"]
print("Choose your choice number: 0 = Male, 1 = Female, 2 = Other")
choice = int(input("Enter your choice number: "))
gender = gender[choice]

age= int(input("Enter your age: "))
height = int(input("Enter your height in cm: "))

about = input("Write something about yourself: ")

my_tuple = (first_name, last_name, gender, age, height, about)

list(my_tuple)
print(my_tuple)