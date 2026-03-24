# Main menu
import random

while True:
    print('MAIN MENU')
    print('1. For-Loops')
    print('2. While-Loops')
    print('3. Fibonacci Sequence')
    print('4. Detect Prime Number')
    print('5. Exit')

    choice = input('Enter your choice: ')
    if choice.isdigit() and int(choice) <= 5 and int(choice) >= 1:
        choice = int(choice)
        if choice == 1:
            print('FOR-LOOPS SUBMENU')
            print('1. Counting Sheep')
            print('2. Rocket Lauch Countdown')
            print('3. Module Average') 
            print('4. Factorial Calculation')
            print('5. Back to main menu')

            choice = input('Enter your choice: ')
            if choice.isdigit() and int(choice) <= 5 and int(choice) >= 1:
                choice = int(choice)
                if choice == 1:
                    print('Counting Sheep')
                    for i in range(10):
                        print(f'Sheep {i + 1}')
                    print('\n')
                
                elif choice == 2:
                    print('Rocket Lauch Countdown')
                    for i in range(10, 0, -1):
                        print(i)
                    print('Liftoff!')
                    print('\n')

                elif choice == 3:
                    moduleCount = int(input('Enter the number of modules: '))
                    total = 0
                    for i in range(moduleCount):
                        moduleMark = float(input(f'Enter module number {i + 1}: '))
                        total += moduleMark
                    average = total / moduleCount
                    print(f'Average: {average}')
                    if average >= 60:
                        print('You can apply for honours')
                    else:
                        print('You cannot apply for honours')
                    print('\n')
                        
                elif choice == 4:
                    print('Factorial Calculation')
                    num = int(input('Enter a number: '))
                    factorial = 1
                    for i in range(1, num + 1):
                        factorial *= i
                    print(f'Factorial: {factorial}:')
                    print('\n')

                elif choice == 5:
                    pass
            else:
                print('Invalid choice. Please try again.')


        elif choice == 2:
            # print('While-Loops')
            while True:
                print('1. Password Checker')
                print('2. Entering a positive number')
                print('3. Climbing the mountin ')
                print('4. Guess the number')
                print('5. Back to main menu')

                choice = input('Enter your choice: ')
                if choice.isdigit() and int(choice) <= 5 and int(choice) >= 1:
                    choice = int(choice)
                    if choice == 1:
                        password = input('Enter your password: ')
                        while password != 'P@55w0rd123!':
                            print('Access denied please try again!')
                            password = input('Enter your password: ')
                        print('Access GRANTED!')
                        print('\n')

                    elif choice == 2:
                        num = float(input('Enter a positive number: '))
                        if num <= 0:
                            print('Invalid input. Please enter a positive number.')
                        while num <= 0:
                            num = float(input('Enter a positive number: '))
                            print('Invalid input. Please enter a positive number.')
                        print('Number accepted')
                        print('\n')

                    elif choice == 3:
                   # print('Climbing the mountin ')
                        topDistance = 5000
                        time = 0
                        while topDistance > 0:
                            # validation
                            while True:
                                day = int(input(f'Enter meters climbed in day {time + 1} (between 300 and 700): '))
                                if day > 300 and day <= 700:
                                    break

                                else:
                                    print('Invalid input. Please enter a number between 300 and 700')

                            time += 1
                            topDistance -= day
                            
                            if topDistance <= 0:
                                print(f'You reached the peak in {time} days!')
                            else:
                                topDistance += 150
                                print(f'You still have to climb {topDistance} meters!')
                        print('\n')
                    
                    elif choice == 4:
                        print('Guess the number')
                        randNum = random.randint(1, 100)
                        attempts = 0
                        while True:
                            guess = int(input('Guess the number (1-100): '))
                            attempts += 1
                            
                            if guess >= 1 and guess <= 100:
                                if randNum == guess:
                                    print(f'Congratulations! You guessed it in {attempts} tries')
                                    break
                                elif randNum > guess:
                                    print('Too low')
                                elif randNum < guess:
                                    print('Too high')
                            else:
                                print('Invalid input try again')

                    elif choice == 5:
                        break

        elif choice == 3:
            terms = int(input('Enter the number of terms: '))
            fib1 = 0
            fib2 = 1
            if terms == 1:
                print(fib1)
            else:
                print(fib1)
                for i in range(terms - 1):
                    calc =  fib1 + fib2
                    fib1 = fib2
                    fib2 = calc
                    print(fib1)
            print('\n')

        elif choice == 4:
            while True:
                num = int(input('Enter a number: '))
                if num <= 1:
                    print(f'{num} is not a prime number.')
                else:
                    for i in range(2, num):
                        if num % i == 0:
                            print(f'{num} is not a prime number.')
                            break
                    else:
                        print(f'{num} is a prime number.')
                        break
                        
                
        elif choice == 5:
            print('goodbye!')
            exit()

    else:
        print('Invalid choice. Please try again.')