my_set = {1,2,3,4}

my_set.add(5)
print("Updated Set: ", my_set)

set1 = my_set
set2 ={2,4,4,6}

print("\nSet1 ", set1)
print("Set2 ", set2)
print("Difference")
print(set1.difference(set2))
print("Symmetric Difference")
print(set1.symmetric_difference(set2))