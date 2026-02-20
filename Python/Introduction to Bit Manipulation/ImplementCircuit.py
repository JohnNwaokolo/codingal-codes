def circuitproblem(A, B, C1):
    AND1 = A & B
    OR1 = B | C
    AND2 = B & C
    AND3 = OR1 & AND2

    Q = AND1 | AND3

    print("\nOutput Q is ",Q,".\n")

A = int(input("A: "))%2
B = int(input("B: "))%2
C = int(input("C: "))%2

circuitproblem(A, B, C)
