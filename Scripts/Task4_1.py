# main menu
while True:
    print('MAIN MENU')
    print('1. While loop programs')
    print('2. Calculate commission')
    print('3. Calculate commision for multiple employees')
    print('4. Sum a specified number of values')
    print('5. Draw a square')
    print('6. For loop programs')
    print('7. Laptop VAT calculation')
    print('8. Exit')

    choice = input('Enter your choice: ')
    if choice.isdigit() and int(choice) <= 8 and int(choice) >= 1:
        choice = int(choice)
        if choice == 1:
            while True:
                print('WHILE LOOP SUBMENU')
                print('1. Count to 10')
                print('2. Count to a value entered by the user')
                print('3. Back to main menu')
                choice = input('Enter your choice: ')
                if choice.isdigit() and int(choice) <= 3 and int(choice) >= 1:
                    choice = int(choice)
                    if choice == 1:
                        for i in range(0,10):
                            print(i + 1)
                        print('\n')

                    elif choice == 2:
                        num = int(input('Enter a number: '))
                        for i in range(0, num):
                            print(i + 1)
                        print('\n')
                   

                    elif choice == 3:
                        break
                else:
                    print('Invalid choice. Please try again.')
            
        elif choice == 2:
            sales =  int(input('Enter the sales amount: '))
            commision = float(input('Enter comission rate (as a decimal): '))
            amount = sales * commision
            print(f'The commission is: {amount}')


        elif choice == 3:
            print('Calculate commision for multiple employees')
            employeesCount = int(input('Enter the number of employees: '))
            for i in range(employeesCount):
                sales = int(input(f'Enter the sales amount for employee {i + 1}: '))
                commission = float(input(f'Enter the commission rate for employee {i + 1}: '))
                amount = sales * commission
                print(f'The amount of commission for employee {i + 1} is: {amount}')
            print('\n')
            
        elif choice == 4:
           num = int(input('Enter a number of values to sum: '))
           for i in range(num):
            sum = float(input(f'Enter value {i + 1}: '))
            sum += sum  
           print(f'The total sum of the values is: {sum}')
           print('\n')

        elif choice == 5:
            side = int(input('Enter the size of the square: '))
            char = input('Enter the character to draw the square with: ')
            for i in range(side):
                print(char * side)
            print('\n')
            
        elif choice == 6:
            while True:
                print('FOR LOOP SUBMENUS')
                print('1. Count 10')
                print('2. Count to a user-entered value')
                print('3. Count from 100 to 0 in increments of 2')
                print('4. Back to main menu')
                choice = input('Enter your choice: ')
                if choice.isdigit() and int(choice) <= 4 and int(choice) >= 1:
                    choice = int(choice)
                    if choice == 1:
                        for i in range(0,10):
                            print(i + 1)
                        print('\n')

                    elif choice == 2:
                        num = int(input('Enter a number: '))
                        for i in range(0, num):
                            print(i + 1)
                        print('\n')
                   

                    elif choice == 3:
                        for i in range(100, -1, -2):
                            print(i)
                        print('\n')
                    elif choice == 4:
                        break
                else:
                    print('Invalid choice. Please try again.')

        elif choice == 7:
            fixedPrice = 10000
            vat = 0.15
            for i in range(0, 3):
                print(f'Year {i + 1}: R{fixedPrice * (1 + vat):.2f} at {vat * 100}% VAT')
                vat += 0.005
            print('\n')

        elif choice == 8:
            print('Goodbye!')
            exit()
    else:
        print('Invalid choice. Please try again.')
        