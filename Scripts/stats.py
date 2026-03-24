# User inputs
width = int(input('Enter rectangle width: '))
if width <= 0:
    width = int(input('Enter rectangle width: '))

length = int(input('Enter rectangle length: '))
if length <= 0:
    length = int(input('Enter rectangle length: '))
    
while width and length > 0:
    print('Here is your rectangle: ')
    for length in range(length):
        print('*' * width)

    break