def mul(M, N):

    sol = N*M
    return sol
# Iterations = O(1)


def mul2(M, N) :
    
    sol=0
    for i in range(N):
        sol += M
    return sol
# Iterations = O(N)