binary_value = input("Enter a binary value: ")
decimal_value = 0

power = len(binary_value) - 1

for digit in binary_value:
    digit = int(digit)
    ans = digit * 2**power
    decimal_value += ans
    power -= 1

print(f"The Decimal Value of the Binary Number - {binary_value} is = {decimal_value} ")