x="a"

def test():
    global x
    x="z"


print(x)
test()
print(x)