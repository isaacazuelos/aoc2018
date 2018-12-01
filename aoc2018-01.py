from itertools import cycle

lines = open('input1.txt', 'r').readlines()
print(sum(int(l) for l in lines))
nums = list(int(l) for l in lines)

seen = set()
acc = 0

for n in cycle(nums):
    seen.add(acc)
    acc+=n
    if acc in seen:
        print(acc)
        break

    
#print("acc= ", acc, "seen=", seen)
