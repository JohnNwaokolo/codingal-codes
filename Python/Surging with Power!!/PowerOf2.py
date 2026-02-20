def isPowerTwo(x):

    if (x==0):
        return False
    
    else: 
        while (x%2 == 0):
            x /= 2
        
