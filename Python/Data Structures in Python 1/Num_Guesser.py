import random
from colorama import Fore, Style

list_num =[]

for i in range(7):
    num = random.randint(5,50)
    list_num.append(num)

print(list_num)
print("=================")

judge_num = random.choice(list_num)

user_input = int(input("Guess the number chosen by the judges out of the list above: "))

while user_input != judge_num:
    if user_input > judge_num:
      print(Fore.RED +"Your number is higher, try again" + Style.RESET_ALL)
      print("=================")
    
    elif user_input < judge_num:
     print(Fore.GREEN + "Your number is low, try again" + Style.RESET_ALL)
     print("=================")

    user_input = int(input("Guess again: "))

print("=====SUCCESS=====")
    








    




