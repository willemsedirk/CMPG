import math

# global constant
MAX_NUMBERS = 5


# function that calculates the square root and log10 of the total and returns both values
def analyseSum(total):
    square = math.sqrt(total)
    log10 = math.log10(total)
    return square, log10


# main program logic
def main():
    cycle = 0
    total = 0
    for i in range(MAX_NUMBERS):
        cycle += 1
        num = float(input(f'Please enter a postive number #{cycle}: '))
        while num <= 0:
            num = float(input(f'Please enter a postive number #{cycle}: '))
        else:
            total += num
    # tuple unpacking: [square, log10] => square = x , log10 = y
    square, log10_value = analyseSum(total)
    print(f'\t The sum of the numbers \t \t = \t {total: .4f}')
    print(f'\t The square root of the sum \t \t = \t {square: .4f}')
    print(f'\t The log10 of the sum \t \t \t = \t {log10_value: .4f}')


if __name__ == "__main__":
    main()
