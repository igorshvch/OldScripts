print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

from sys import argv

script, filename = argv

print ("We're going to earse %r." % filename)
print ("If you don't want that, hit CTRL-C (^C).")
print ("If you do want that, hit RETURN.")

input("==>?")

print ("Openning the file...")
target = open(filename, "w")

print ("Truncating the file. Goodbye!")
target.truncate()

print ("Now I'm going to ask you for three lines.")
line1 = input("line 1: ==>")
line2 = input("line 2: ==>")
line3 = input("line 3: ==>")

print ("I'm going to write these to the %r." % filename)

target.write(line1 + "\n" + line2 + "\n" + line3 + "\n")
          
print ("And finally, we close it.")
target.close()

should = input("Do I need to print the result? Please print '0' for 'No' and '1' for 'Yes'")

should_i = int(should)

if should_i:
    check = open (filename)
    print (check.read())
    check.close()
print ("Bye!")

print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")