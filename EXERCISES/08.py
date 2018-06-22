print ("*" * 10)
print ("*" * 10)
print ("*" * 10)
formatter = "%r %r %r %r"

print (formatter % (1, 2 ,3 ,4))
print (formatter % ("one", "two", "three", "four"))
print (formatter % (True, False, True, False))
print (formatter % (formatter, formatter, formatter, formatter))
print (formatter % (
    "I had this thing.",
    "That you could type up right.",
    "But it didn't sign.",
    "So I said goodnight."
))
print ("*" * 10)
print ("*" * 10)
print ("*" * 10)