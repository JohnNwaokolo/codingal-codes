
my_dict = {}

my_dict = {1: "apple", 2: "ball"}

my_dict = {"name": "John", 1: [2,4,3]}

my_dict = {"name" : "Jack", "age": 26}

print(my_dict["name"])
print(my_dict)

my_dict["address"]= "Downtown"
print(my_dict)

my_dict.pop("age")
print(my_dict)

print("Address :", my_dict.get("address"))
