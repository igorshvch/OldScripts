print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

from sys import argv

script, filename = argv

txt = open (filename)

print ("Here's your file %r:" % filename, "\n")
print (txt.read() + "\n")

txt.close()

print ("Type the filename again:" + "\n")
file_again = input (')->')

txt_again = open (file_again)

print ("\n" + txt_again.read())

txt_again.close()
          
print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")