print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")

def lets_play (logval1):
    if logval1 != 0:

        people = int (input ("\nPlease type the number of people: "))
        cats = int (input ("Please choose the quantity of cats: "))
        dogs = int (input ("And now please tell the capacity of dogs: "))
        print ("\nWould you like me to provide you with some advices?")
        logval2 = int (input ("Please type '1' for YES or '0' for NO: \n\n"))

        if logval2 == 1:
            if cats > people:
                print ("\nBe aware! Cat's are superior!")
            if people > cats:
                print ("\nLook around. Probably some kitten walks near by.")
            if cats == people:
                print ("\nPeople are cats... Or cats are people...")
            if cats == dogs:
                print ("\nProbably, cats are dogs or vice versa.")
            if cats < dogs and people < cats:
                print ("\nDogs are our allies. Together we will win the cats and will rule the whole world!!!")
        elif bool == 0:
            print ("\nSo, no. Ok, that's fine")
        else:
            print ("\nYor message is incorrect! I can't understand you :-(")

    else:
        print ("\nSome general error has occures! Check the code!")

print ("Let's try something more complicated!")
answer = int (input ("Would you? (1|0 for Y|N): "))
lets_play (answer)

      
print (" ")
print ("-" * 50)
print ("-" * 50)
print (" ")