#   Collatz conjecture script

#   Takes a number (n) and:

#           if it is even divides by two
#           if it is odd multiplies by 3 and adds 1

#   Counts how many steps taken to reach a final outcome of 1

#   Returns the value of the counter

from time import sleep
from IPython.display import clear_output as clear

def collatz(number):

    clear()
    n = number
    c = 0
    
    def output(c,n):
        
        print(f'\nStarting point: {number}\n')
        print(f'\tStep {c}: {n}')
        
        if n == 1:
            print(f'\nCompleted in {c} steps\n')
            #print(f'Time wasted: {c} seconds')
        else:
            pass
            #print(f'\nCompleted in: -- steps')
            #print(f'Time wasted: {c} seconds')
        
        sleep(1)
        clear(wait=True)

    while n > 1:
        
        if n % 2 == 0:
            n = n / 2
            c += 1
            output(c,n)
        
        else:
            n = (n * 3) + 1
            c += 1
            output(c,n)
    
    #output(c,n)
    
collatz(int(input('\nEnter a starting value for the Collatz Conjecture:')))
exit()