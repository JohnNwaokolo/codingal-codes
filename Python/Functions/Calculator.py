def add(x,y):
   return x+y

def subtract(x,y):
   return x-y

def multiply(x,y):
   return x*y

def divide(x,y):
   return x/y

x= int(input("Enter the value of x: "))
y= int(input("Enter the value of y: "))

print (f"Sum: ", add(x,y))
print (f"Subtract: ", subtract(x,y))
print (f"Multiply: ", multiply(x,y))
print (f"Quotient: ", divide(x,y))
