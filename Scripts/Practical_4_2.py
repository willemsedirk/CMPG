# User inputs
while True:

    currentSalary = input('Enter your yearly salary: ')
    print(f'The salary after 0 year is {currentSalary}')

    if currentSalary.isdigit():
        currentSalary = float(currentSalary)
        print(f'The salary after 0 year is {currentSalary: .2f}')

        for i in range(5):
            currentSalary = currentSalary * 1.05
            print(f'The salary after {i + 1} year is {currentSalary: .2f}')
     
        break

    else:
        print('Invalid input!')
