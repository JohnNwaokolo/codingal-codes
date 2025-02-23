lst = ["Apple", "Guava", "Mango", "Banana", "Kiwi"]

print("Length of list", len(lst))
print("First Element", lst[0])
print("Last Element", lst[4])

lst.append("Papaya")
print("Updated List", lst)

lst.remove("Guava")
print("Updated list", lst)

lst.sort()
print("Updated list: ", lst)

lst.pop(1)
print("Updated List: ", lst)

lst.reverse()
print("Reversed List ",lst)

print ("Multiplication on List ", lst*2)

lst= lst[:4]
print("Updated List :",lst)
