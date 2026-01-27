num1 = int(input("Enter First Number: "))
num2 = int(input("Enter Second Number: "))

start = max(num1, num2)
lcm = start

while True:
    if lcm % num1 ==0 and lcm % num2 == 0:
        print(f"LCM is = {lcm}")
        break

    lcm += 1

