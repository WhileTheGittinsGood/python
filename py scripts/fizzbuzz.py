# FizzBuzz

def fizzbuzz(num):

    n = num

    while n > 0:

        if n % 3 == 0 and n % 5 == 0:

            print('fizzbuzz')
            n -= 1

        elif n % 3 == 0:

            print('fizz')
            n -= 1

        elif n % 5:

            print('buzz')
            n -= 1

        else:

            print(n)
            n -= 1

fizzbuzz(int(input('enter a number for fizzbuzz to start with:')))