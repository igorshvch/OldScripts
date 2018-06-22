# Compares two lists and finds mismatchings

def ctb (first_list, second_list, count = 0):
	if len(first_list) < len(second_list):
		count = len(first_list)
	else:
		count = len(second_list)
	for i in range(0, count - 1):
		if first_list[i] != second_list[i]:
			sampfirst = ' '.join(first_list[i-5:i+1])
			sampsec = ' '.join(second_list[i-5:i+1])
			print ('-'*20)
			print ('Это ИНДЕКС: %d\n\nЭто слово из ПЕРВОГО фрагмента: %s\nЭто слово из ВТОРОГО фрагмента: %s\n\nКусок ПЕРВОГО фрагмента:\n%s\nКусок ВТОРОГО фрагмента:\n%s\n\nSTOP' % (i+1, first_list[i], second_list[i], sampfirst, sampsec))
			print ('-'*20)
			decision = input("чтобы продолжить, нажмите '1': ")
			if decision == '1':
				continue
			else:
				break
	print ('Окончание проверки')
	print ('STOP')

# Simplyfices convertion text fragments to lists

def nmls ():
	ls = input('type here: ')
	ls = ls.split()
	return ls

