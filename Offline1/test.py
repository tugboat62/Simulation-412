from lcgrand import LCG

# Path: test.py
# Compare this snippet from lcgrand.py:
# class LCG:

# lcg = LCG()
# for i in range(1, 200):
#     print(i)
#     print(lcg.lcgrand(i))
a = [1, 2, 3, 4, 5]

# for i in range(1, 6):
#     print(a[-i])    
    
# loop in reverse order
for i in reversed(range(6)):
    print(i)

a.sort(reverse=True)
print(a)
a.__len__()