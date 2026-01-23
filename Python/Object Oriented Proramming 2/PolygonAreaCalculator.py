class Shapes:
    def __init__(self, name, sides=0):
        self.name = name
        self.sides = sides 
           
    def introduce(self):
        print(f"This is a {self.name}")
        return f"This {self.name} has {self.sides} sides."

class Rectangle(Shapes):
    def __init__(self, length, width):
        super().__init__("Rectangle", 4)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width
    

class Square(Shapes):
    def __init__(self, length):
        super().__init__("Square", 4)
        self.length = length

    def area(self):
        return self.length ** 2
    
Rectangle1 = Rectangle(4, 6)
Rectangle1.introduce()
print(f"Area of Rectangle: {Rectangle1.area()}")

Square1 = Square(5)
Square1.introduce()
print(f"Area of Square: {Square1.area()}")