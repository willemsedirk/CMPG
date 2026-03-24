# User input

while True:
    num = input('Give a number between 0 and 11, enter 0 to stop: ')
    multi = 0

    if num == '0':
        break

    elif num.isdigit():
        print(f'Multiplication table: {num}')
        for i in range(1, 11):
            answer = int(num) * i
            print(f'{i} x {num} = {answer}')

    else:
        print('Invalid input!')
