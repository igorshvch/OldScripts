print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

def print_two (*args):
    arg1, arg2 = args
    print ("arg1: %r, arg2: %r" % (arg1, arg2))

def print_two_again (arg1, arg2):
    print ("arg1: %r, arg2: %r" % (arg1, arg2))

def print_one (arg1):
    print ("arg1: %r" % arg1)

def print_none():
    print ("There is nothing to print here!")

print_two ("Igor", "Shevchenko")
print_two_again ("Igor", "Shevchenko")
print_one ("Hey!")
print_none()

print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")