from random import choice

for i in range(99 - 1):
    print(choice(["1", "2"]), end=",")
print(choice(["1", "2"]), end="")
