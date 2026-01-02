class Robot:
    def __init__(self, name):
        self.name = name

    def introduce_self(self):
        print(f"Hello, my name is {self.name}.")

robot1 = Robot("R2-D2")
robot2 = Robot("C-3PO")

robot1.introduce_self()
robot2.introduce_self()