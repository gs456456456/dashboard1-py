a = 3

def x():
    global a
    a = 4
    return a

print(x())
