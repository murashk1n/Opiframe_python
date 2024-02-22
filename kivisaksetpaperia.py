# Kivi sakset paperia
import random

def checkWhoWin(a, b):
	if a == 'k' and b == 's' or a == 's' and b == 'k':
		return 'k'
	elif a == 'k' and b == 'p' or a == 'p' and b == 'k':
		return 'p'
	elif a == 's' and b == 'p' or a == 'p' and b == 's':
		return 's'

random = random.randint(1,3)
print("Welcome to kivi sakset paperia\n\n")
answer = input("\nYour choise: ")
compChoise = ''

match random:
    case 1  : 
      compChoise = 'k'
    case 2 : 
      compChoise = 's'   
    case 3 : 
      compChoise = 'p'

	
print(f"\nComputer choise: {compChoise}")

if compChoise == answer:
	print("\nDead heat\n")
elif answer == checkWhoWin(answer,compChoise):
	print("\nYou win!\n")
elif compChoise == checkWhoWin(answer, compChoise):
	print("\nComputer win!\n");
else:
	print("\nIllegal choice\n")