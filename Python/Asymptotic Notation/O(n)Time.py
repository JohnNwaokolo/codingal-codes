def OnTime(n):
    literation = 0
    for i in range(1, n+1):
        literation += 1  
        print("When n is", n, "iteration is", literation)

OnTime(10)
OnTime(20)
OnTime(42)

print("\nWith increase in 'n', the time taken by the computer increases linearly.")