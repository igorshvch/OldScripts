print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

def cheese_and_crackers (cheese_count, boxes_of_crackers):
    print ("You have %d cheese!" % cheese_count)
    print ("You have %f boxes of crackers!" % boxes_of_crackers)
    print ("Man thst's enough for the party, ya!" + "\nGet blanket!")

print ("We can just give the function numbers directly!")
cheese_and_crackers (20, 40)

print ("\nOR, we can use variables from our script:")

amofch = 100
amofbox = 2304

cheese_and_crackers (amofch, amofbox)

print ("\nWe can even do math inside too:")

cheese_and_crackers (100+204452, 2341315/56)

print ("\nAnd we can combine the two, variables and math:")
cheese_and_crackers (100 + amofch, (4560/3) + amofbox)

print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")