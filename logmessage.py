DEBUG = False

def log(*msg):
    if DEBUG:
        for i in msg:
            print(i, end="")
        print()
