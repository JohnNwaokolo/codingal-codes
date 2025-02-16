n = int(input("Enter number to check: "))
 
stg = str(n)
num_digits = len(stg)

armstrong_sum = sum(int(digit)**num_digits for digit in stg)

if armstrong_sum == n :
    print(f"{n} is an armstrong number")
else:
     print(f"{n} is not an armstrong number")