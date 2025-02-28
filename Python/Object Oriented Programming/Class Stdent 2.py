class student:
    grade = int(input("Enter your grade: "))
    name = input("Enter your name: ")

    def introduction(self):
        print("Hi I am a student")

    def details(self):
        print("My name is ",self.name)   
        print("I study in Grade", self.grade)

ob = student()
ob.introduction()
ob.details()