def myfunction(n):
  for i in range(0,n+1):
     print("First Loop")
  j = 1
  while (j <= n + 1):
     print("Second Loop ",j)
  j=j*2
  for i in range(0,100):
     print("Third loop")

# Time Complexity:
# First loop  -> O(n) because it runs 'n' times
# Second loop -> O(log n) bxecause j is multiplied by 2 in each iteration
# Third loop  -> O(1) because it runs a constant 100 times
# Overall Time Complexity -> O(n) + O(log n) + O(1) = O(n) because O(n) is the dominant term
