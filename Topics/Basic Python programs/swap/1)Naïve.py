P = int(input("Please Enter Value for P: "))
Q = int(input("Please Enter Value for Q: "))

temp_1 = P
P = Q
Q = temp_1

print()
print("The value of P after swapping", P)
print("The value of Q after swapping", Q)