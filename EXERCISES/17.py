print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

from sys import argv
from os.path import exists

script, from_file, to_file = argv

print ("Coping from %s to %s" % (from_file, to_file))
indata = open(from_file).read()

print ("The input file is %d bytes long" % len(indata))

print ("Does the output file exists? %r" %exists(to_file))
print ("If ready, hit ENTER to continue, CTRL-C to abort.")
input("Y|N?-->")

out_file = open(to_file, "w")
out_file.write(indata)

print ("All right, all done!")

print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")