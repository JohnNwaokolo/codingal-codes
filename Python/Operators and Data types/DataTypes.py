name="John"
is_student=True
weight=38.5
age=15

print ("Name:",name)
print ("Data type of name is:",type(name))
print ("is_student;",is_student)
print ("Data type for is_student is:",type(is_student))
print ("Weight:",weight)
print ("Data type of weight is:",type(weight))
print ("Age:",age)
print ("Data type of age is:",type(age))

print("\n After Typecasting")
age=str(age)
print(age)
print("Data type for age is now:",type(age))
weight=int(weight)
print(weight)
print("Data type for weight is now:",type(weight))
age=float(age)
print(age)
print("Data type for age is now:",type(age))
