class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def information(self):
        print(f"I am a cat.\n My name is {self.name}.\n I am {self.age} years old. ") 

    def makeSound(self):
        print ("Meow")   

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def information(self):
        print(f"I am a dog.\n My name is {self.name}.\n I am {self.age} years old. ") 

    def makeSound(self):
        print ("Woof woof")   
        
obj_dog = Dog("Jake", 4)
obj_cat = Cat("Cassy", 8)

obj_dog.information()
obj_dog.makeSound()

obj_cat.information()
obj_cat.makeSound()
