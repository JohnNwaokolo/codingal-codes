workdays = 328
absentdays = int(input("Enter the number of days absent: "))
totaldays = (workdays-absentdays)/workdays*100

if totaldays <= 75 :
    print("Oops, you didn't meet up to our requirement, so you are not legible for this examination.")

else:
    print("Congratulations, you can write this exam.")    
  