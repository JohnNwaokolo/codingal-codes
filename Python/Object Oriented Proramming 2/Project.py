class Shapes:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"This is a {self.name}")

    

Shape1= Shapes("Rectangle")
Shape1.introduce()