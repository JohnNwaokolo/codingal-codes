from math import sqrt 
input = int(input("Enter a number: "))
for k in range(2, int(sqrt(input))+1):
        
    # if divisible by any number it is a non prime number
    if (input % k) == 0:
        print(input, "is not a prime number")
        break
    else:
        print(input, "is a prime number")
        break