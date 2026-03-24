# User inputs
position = int(input('Enter the value for the ammout of places(N): '))

# variables
count = 0
sumNum = 0

for i in range(0, position * 2, 2):
    count += 2
    sumNum += count

print(f'The sum of the first 4 even numbers is {sumNum}')
