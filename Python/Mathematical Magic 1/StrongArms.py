number = int(input("Enter a number: "))

digits = len(str(number))
resultNumber = 0

temp = number
while temp > 0:
    digit = temp % 10
    resultNumber += digit ** digits
    temp //= 10

if number == resultNumber:
    print(f"{number} is an Armstrong number")
else:
    print(f"{number} is not an Armstrong number")