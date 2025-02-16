def rec_func(n):
    if n == 1:
       return n
    else:
        return n*rec_func(n-1)

num = int(input("Enter the number: "))

if num < 0 :
    print("Sorry, negative numbers dont have factorials")
elif num==0 :
   print("The factorial of 0 is 1")
else :
    print(f"The factorial of {num} is {rec_func(num)}")