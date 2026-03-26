import random

# Variables
flag = True


# fucntion for picking a random number and returns that value
def guess_number():
    num = random.randint(1, 100)
    return num


# main program logic
def main():
    random.seed(10)
    print('Guess the Number Game')

    attempts = 0
    num = guess_number()

    while True:
        guess = input("Guess number 1 - 100 (or 0 to quit): ")

        attempts += 1
        if not guess.isdigit():
            print('Invalid Input!')

        elif guess == '0':
            print('Goodbye!')
            exit()

        else:
            if int(guess) == num:
                print(f'You guesses {num} in {attempts} attempts.')
                exit()

            elif int(guess) > num:
                print('Too high')

            else:
                print('Too low')


main()
