print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

def add (a, b):
    print ("ADDING %d + %d" % (a, b))
    return a+b

def subtract (a, b):
    print ("SUBTRACTING %d - %d" % (a, b))
    return a - b

def multiply (a, b):
    print ("MULTIPLYING %d * %d" % (a, b))
    return a*b

def divide (a, b):
    print ("DIVIDING %d / %d" % (a, b))
    return a/b

print ("Let's do some math with fust functions!")

age = add (30, 5)
height = subtract (78, 4)
weight = multiply (90, 2)
iq = divide (100, 2)

print ("Age: %d,\nHeight: %d,\nWeight: %d,\nIQ: %d." % (age, height, weight, iq))

print ("\nHere is a puzzle")

what = add (age, subtract (multiply (weight, divide (iq, 2)), height))

print ("That becomes: ", what, "Can you do it by hand?")

print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")