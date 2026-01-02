class Expression:
    def __init__(self, num1, num2, num3):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3

    def add(self):
        sum = self.num1 + self.num2 + self.num3
        print("The sum of the three numbers is:", sum)  
        return sum
        

eqn1 = Expression(5, 10, 15)
result = eqn1.add()